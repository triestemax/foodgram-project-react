from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


from foodgram.settings import LENGTH_NAME
from users.models import User


class Ingredients(models.Model):
    """Модель данных об ингредиентах"""

    name = models.CharField('Название ингредиента', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name[:LENGTH_NAME]


class Tag(models.Model):
    """Модель данных тегов"""

    name = models.CharField('Название тега', max_length=200,)
    color = models.CharField(
        'Цвет тега',
        max_length=7,
        null=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле должно содержать HEX-код выбранного цвета.'
            )
        ]
    )
    slug = models.SlugField(
        'Слаг тега',
        max_length=200,
        unique=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name[:LENGTH_NAME]


class Recipes(models.Model):
    """Модель рецептов"""

    name = models.CharField(
        'Название рецепта блюда',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание приготовления блюда',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsInRecipe',
        verbose_name='Используемые ингредиенты в рецепте',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsInRecipe',
        verbose_name='Используемые теги в рецепте',
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        'Время приготовления блюда в минутах',
        validators=(MinValueValidator(1),),
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name[:LENGTH_NAME]


class IngredientsInRecipe(models.Model):
    """Модель для связи ингредиентов с рецептами"""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта',
        help_text='Необходимо название рецепта',
    )

    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты рецепта блюда',
        help_text='Необходим ингредиент',
    )
    amount = models.IntegerField(
        'Количество ингредиента, требуемого для приготовления',
        validators=(MinValueValidator(1),),
    )

    class Meta:
        verbose_name = 'Ингредиенты для рецептов'
        verbose_name_plural = 'Ингредиенты для рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredientsinrecipes',
            )
        ]

    def __str__(self):
        return f'Для {self.recipe} требуется {self.amount} {self.ingredient}.'


class TagsInRecipe(models.Model):
    """Модель для связи тегов с рецептами"""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта',
        help_text='Необходимо название рецепта',
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги для рецепта',
        help_text='Необходим тег',
    )

    class Meta:
        verbose_name = 'Тэги для рецептов'
        verbose_name_plural = 'Тэги для рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_tagsinrecipes',
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.tag}.'


class Favourite(models.Model):
    """Модель для добавления рецепта в избранное"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='Зарегистрированный пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite',
            )
        ]

    def __str__(self):
        return f'{self.user.username} добавил в избранное: {self.recipe.name}.'


class Shopping_cart(models.Model):
    """Модель для добавления ингредиентов рецепта в корзину"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Зарегистрированный пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Ингредиенты рецепта для списка покупок'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            )
        ]

    def __str__(self):
        return (f'{self.user.username} добавил рецепт '
                f'{self.recipe.name} для списка покупок.')
