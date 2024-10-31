import pytest
from accounts.serializers import UserSerializer
from accounts.models import User

@pytest.mark.django_db
class TestUserSerializer:

    # Verifica se o serializer é válido com dados corretos.
    def test_valid_user_data(self):
        data = {
            "name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password123"
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
    
    # Testa se o serializer retorna erro ao fornecer um email inválido.
    def test_invalid_email_format(self):
        data = {
            "name": "Test User",
            "username": "testuser",
            "email": "invalid-email",
            "password": "Password123"
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    # Testa se o serializer valida corretamente a complexidade da senha.
    def test_password_requirements(self):
        data = {
            "name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "simplepass"
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors
    
    # Testa se o serializer cria o usuário corretamente.
    def test_create_user(self):
        data = {
            "name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password123"
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert isinstance(user, User)
        # Verifica a criptografia da senha
        assert user.check_password(data["password"]) 
