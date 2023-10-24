from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet

from .views import IngredientsViewSet, RecipeViewSet, SaveCart, TagViewSet

User = get_user_model()

router = DefaultRouter()

app_name = 'api'

router.register('users', UsersViewSet, basename='users')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('recipes/download_shopping_cart/', SaveCart.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls'))
]
