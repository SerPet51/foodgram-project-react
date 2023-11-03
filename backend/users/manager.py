from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError('Поле email не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        """
        Создание и сохранение суперпользователя с указанным email и password.
        """
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser'):
            return self.create_user(email, password, username, **extra_fields)
        raise ValueError('Суперпользователь должен иметь is_superuser=True.')
