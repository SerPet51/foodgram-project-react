from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from foodgram.pagination import LimitPageNumberPaginator
from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)
from .permissions import AuthorOrReadOnly
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeCreateSerializer,
    RecipeGetSerializer, ShoppingCartSerializer, TagSerializer)


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RecipeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=400)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = RecipeGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPaginator

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def favorite_and_shopping_cart_add(model, user, recipe):
        model_create, create = model.objects.get_or_create(
            user=user, recipe=recipe
        )
        if create:
            if type(model) == 'Favorite':
                serializer = FavoriteSerializer()
            else:
                serializer = ShoppingCartSerializer()
            return Response(
                serializer.to_representation(instance=model_create),
                status=status.HTTP_201_CREATED
            )

    @staticmethod
    def favorite_and_shopping_cart_delete(model, user, recipe):
        model.objects.filter(recipe=recipe, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        filter_backends=DjangoFilterBackend,
        filterset_class=RecipeFilter
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            return self.favorite_and_shopping_cart_add(
                Favorite, user, recipe)
        if request.method == 'DELETE':
            return self.favorite_and_shopping_cart_delete(
                Favorite, user, recipe)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            return self.favorite_and_shopping_cart_add(
                ShoppingCart, user, recipe)
        if request.method == 'DELETE':
            return self.favorite_and_shopping_cart_delete(
                ShoppingCart, user, recipe)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(IsAuthenticated,)
            )
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        ingredients = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))
        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.txt"'
        return response
