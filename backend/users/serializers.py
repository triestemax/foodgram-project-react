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

    def validate_username(self, usernamecreate):
        if usernamecreate == 'me':
            raise serializers.ValidationError(
                {'detail': 'Нельзя использовать me!'},
                code=status.HTTP_400_BAD_REQUEST
            )
        elif User.objects.filter(username=usernamecreate):
            raise serializers.ValidationError(
                {'detail': 'Пользователь с таким никнеймом уже существует!'},
                code=status.HTTP_400_BAD_REQUEST,
            )
        return usernamecreate

    def validate_email(self, emailcreate):
        if User.objects.filter(email=emailcreate):
            raise serializers.ValidationError(
                {'detail': 'Пользователь c таким адресом уже существует!'},
                code=status.HTTP_400_BAD_REQUEST
            )
        return emailcreate


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('email', 'username')

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
