from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

# User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'role']

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role']
        )

# Переопределение стандартного TokenObtainPairSerializer -
# По умолчанию сериализатор ожидает поля username и password.
# Делаем кастомный сериализатор, где вместо username будет использоваться email.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # username_field = User.EMAIL_FIELD # Это атрибут, который по умолчанию возвращает имя поля email
                                        # для стандартной модели auth.User. С использованием нашего кастомного юзера, это поле
                                        # всё ещё корректно указывает на 'email'
    # Можно указать явно как
    username_field = 'email' # Логинимся по email

    def validate(self, attrs):
        # Переименуем поле email -> username для совместимости с базовым классом
        attrs['username'] = attrs.get('email', None)
        return super().validate(attrs)