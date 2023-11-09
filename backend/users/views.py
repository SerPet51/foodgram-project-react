from djoser.views import TokenCreateView, UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from foodgram.pagination import LimitPageNumberPaginator
from recipes.serializers import SubscriptionSerializer
from .models import CustomUser, Follow
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """ВьюСет пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )
    pagination_class = LimitPageNumberPaginator

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['author']:
            raise ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscriptionSerializer(
            instance.author, context={'request': request}
        ).data


class CheckBlockAndTokenCreate(TokenCreateView):
    """Вью для проверки пользователя на блокировку"""
    def _action(self, serializer):
        if serializer.user.is_block:
            return Response(
                {'ERROR': 'Данный пользователь заблокирован!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super()._action(serializer)
