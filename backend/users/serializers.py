from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status

from users.models import Subscribe, User
from recipes.models import Recipes


class UserSerializer(UserSerializer):
    """Сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'password')

    def validate(self, data):
        """Проверяет наличие пользоваталей с введенным email и именем
        и корректность заполнения имени пользователя."""
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким адресом электронной почты уже существует!'
            )
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с такой учетной записью уже существует!'
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'recipes_count',
            'recipes',
        )
        read_only_fields = ('email', 'username')

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                detail='Вы уже подписаны на этого автора!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise serializers.ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeReadShortSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializer.data

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Subscribe.objects.filter(user=user, author=obj).exists()


class RecipeReadShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
