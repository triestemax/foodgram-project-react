from django.contrib import admin

from recipes.models import (
    Ingredients, Tag,
    Recipes, IngredientsInRecipe,
    TagsInRecipe,
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
    list_display = ('id', 'name', 'author', 'in_favorites')
    readonly_fields = ('in_favorites',)
    list_filter = ('name', 'author',)

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@admin.register(TagsInRecipe)
class agsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag')
    list_editable = ('recipe', 'tag')

'''
@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(models.Shopping_cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
'''
