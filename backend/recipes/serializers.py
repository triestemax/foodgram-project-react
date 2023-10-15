from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status

from recipes.models import (
    Ingredients,
    IngredientsInRecipe,
    Recipes,
    Tag,
    Favourite,
    Shopping_cart,
)
from users.serializers import UserSerializer


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов."""

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit',)


class TagsSerializer(serializers.ModelSerializer):
    """Сериалайзер для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientsInRecipeReadSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )
    amount = serializers.ReadOnlyField(source='amount')

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name',
                  'measurement_unit', 'amount')


class RecipesReadSerializer(serializers.ModelSerializer):
    """Сериалайзер для чтения рецептов."""
    author = UserSerializer(read_only=True)
    tags = TagsSerializer(read_only=True, many=True,)
    ingredients = IngredientsInRecipeReadSerializer(
        source='recipes',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Favourite.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Shopping_cart.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        )


class IngredientsInRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipesCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания или обновления рецептов."""
    ingredients = IngredientsInRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipes
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        if not ingredients:
            raise serializers.ValidationError(
                detail='Для рецепта необходимо добавить ингредиенты!',
                code=status.HTTP_400_BAD_REQUEST
            )
        ingredients_unique_list = []
        for ingredientinrecipe in ingredients:
            ingredient = get_object_or_404(
                Ingredients,
                id=ingredientinrecipe['id']
            )
            amount = ingredientinrecipe['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError(
                    {'detail': 'Количество должно быть больше 0!'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            elif ingredient in ingredients_unique_list:
                raise serializers.ValidationError(
                    {'detail': 'Ингредиенты не должны повторяться!'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            else:
                ingredients_unique_list.append(ingredient)
        if not tags:
            raise serializers.ValidationError(
                {'detail': 'Должен быть хотя бы один тег!'},
                code=status.HTTP_400_BAD_REQUEST
            )
        tags_unique_list = []
        for tag in tags:
            if tag in tags_unique_list:
                raise serializers.ValidationError(
                    {'detail': 'Теги не должны повторяться!'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            tags_unique_list.append(tag)
        return data

    @transaction.atomic
    def create_ingredients_amounts(self, ingredients, recipe):
        IngredientsInRecipe.objects.bulk_create(
            [IngredientsInRecipe(
                ingredient=Ingredients.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.create_ingredients_amounts(recipe=recipe, ingredients=ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amounts(
            recipe=instance,
            ingredients=ingredients
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipesReadSerializer(instance, context=context).data


class RecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для рецептов без ингредиентов."""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipes
        fields = ('id', 'name',
                  'image', 'cooking_time')
