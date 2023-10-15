from django.contrib import admin

from recipes.models import (
    Favourite,
    Ingredients,
    IngredientsInRecipe,
    Shopping_cart,
    Tag,
    TagsInRecipe,
    Recipes,
)


@admin.register(Ingredients)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'in_favourites')
    readonly_fields = ('in_favourites',)
    list_filter = ('name', 'author',)

    @admin.display(description='Количество рецептов в избранном')
    def in_favourites(self, obj):
        return obj.favourite.count()


@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@admin.register(TagsInRecipe)
class TagsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag')
    list_editable = ('recipe', 'tag')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(Shopping_cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')
