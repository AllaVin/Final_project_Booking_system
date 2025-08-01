from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
                Создание обычного пользователя.
                - Email обязателен.
                - Пароль хэшируется.
                - Дополнительные поля передаются через extra_fields.
                """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
                Создание суперпользователя.
                - Принудительно устанавливаются флаги is_staff и is_superuser.
                - Выполняется проверка этих флагов.
                """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# --- Кастомная модель пользователя ---
class User(AbstractUser):
    # Роли пользователей: арендатор или арендодатель
    ROLE_CHOICES = [
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
    ]

    # Убираем стандартное поле username (используем email для входа)
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Указываем, что для логина используется email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # убираем обязательные поля кроме email

    objects = UserManager()  # Подключаем кастомный менеджер

    class Meta:
        db_table = 'user' # имя таблицы в БД

    def __str__(self):
        return self.email # Отображение пользователя в админке — по email
