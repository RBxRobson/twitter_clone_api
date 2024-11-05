import pytest
from accounts.serializers import UserSerializer
from accounts.models import User
from accounts.factories import UserFactory  # Importe a factory

@pytest.mark.django_db
class TestUserSerializer:
    # Verifica se o serializer é válido com dados corretos.
    def test_valid_user_data(self):
        user = UserFactory.build()  # Cria um usuário com dados de teste
        data = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "password": "Password123"
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid(), serializer.errors  # Exiba os erros se não for válido
    
    # Testa se o serializer retorna erro ao fornecer um email inválido.
    def test_invalid_email_format(self):
        user = UserFactory.build()  # Cria um usuário com dados de teste
        data = {
            "name": user.name,
            "username": user.username,
            "email": "invalid-email",
            "password": "Password123"
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    # Testa se o serializer valida corretamente a complexidade da senha.
    def test_password_requirements(self):
        user = UserFactory.build()  # Cria um usuário com dados de teste
        data = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "password": "simplepass"
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors
    
    # Testa se o serializer cria o usuário corretamente.
    def test_create_user(self):
        user = UserFactory.build()  # Cria um usuário com dados de teste
        data = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "password": "Password123"
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid(), serializer.errors  # Exiba os erros se não for válido
        user_instance = serializer.save()
        assert isinstance(user_instance, User)
        # Verifica a criptografia da senha
        assert user_instance.check_password(data["password"])
