from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Ingredients, IngredientsInRecipe, Recipes, Tag
from users.serializers import UserSerializer


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit',)


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientsInRecipeReadSerializer(serializers.ModelSerializer):
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
    author = UserSerializer(read_only=True)
    tags = TagsSerializer(read_only=True, many=True,)
    ingredients = IngredientsInRecipeReadSerializer(
        source='recipes',
        many=True,
    )
    #is_favorited = serializers.SerializerMethodField()
    #is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            #'is_favorited',
            #'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class IngredientsInRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipesCreateSerializer(serializers.ModelSerializer):

    ingredients = IngredientsInRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    text = serializers.CharField(source='description')
    cooking_time = serializers.CharField(source='cook_time')

    class Meta:
        model = Recipes
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )
