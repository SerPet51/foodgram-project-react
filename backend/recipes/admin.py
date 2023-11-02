from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_filter = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')

    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('recipe', 'user')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('recipe', 'user')
