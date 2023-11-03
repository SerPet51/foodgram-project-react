from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import CustomUser
from users.views import CustomUserViewSet


class UserTests(APITestCase):
    def setUp(self) -> None:
        CustomUser.objects.create(
            email='test@test.ru',
            username='User1',
            password='password',
            first_name='Test1_first',
            last_name='Test1_last'
        )

    def test_create_delete_user(self) -> None:
        """тест создания юзера"""
        url = reverse('users:users-list')
        data = {
            'email': 'lora@lora.ru',
            'username': 'LoraFirst',
            'password': '123Qwerty321',
            'first_name': 'Lora',
            'last_name': 'Snider',
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(id=2).username, 'LoraFirst')

        user = CustomUser.objects.get(username='LoraFirst')
        url = reverse('users:users-detail', kwargs={'id': user.id})

        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        print(response)
        # print(response)
        # self.assertEqual(CustomUser.objects.count(), 1)

        # user = CustomUser.objects.get(username='LoraFirst')
        # self.client.force_login(user)
        # response = self.client.delete(url + 'me/', )
        # print(response)
        # self.assertEqual(response.status_code, status.)


    # def test_subscribe(self):
    #     url = 'http://127.0.0.1:8000/api/users/1/subscribe/'

