from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientSearchFilter(filters.FilterSet):
    """Фильтр для поиска ингредиентов во время создания рецепта"""
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    """Фильтрует рецепты по избранному, списку покупок и тегам"""
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='favorite_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='shopping_cart_filter'
    )
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    def favorite_filter(self, queryset, name, value):
        recipes = Recipe.objects.filter(favorites__user=self.request.user)
        return recipes

    def shopping_cart_filter(self, queryset, name, value):
        recipes = Recipe.objects.filter(shopping_cart__user=self.request.user)
        return recipes

    class Meta:
        model = Recipe
        fields = ['author']
