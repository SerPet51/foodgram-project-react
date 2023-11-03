from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework import routers

from .views import CheckBlockAndTokenCreate, CustomUserViewSet


router = routers.SimpleRouter()
router.register(r'users', CustomUserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    path('auth/token/login/', CheckBlockAndTokenCreate.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    path('', include(router.urls))
]
