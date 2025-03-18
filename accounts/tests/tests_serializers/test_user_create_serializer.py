import pytest
from accounts.serializers import UserCreateSerializer
from core.utils import create_user
from accounts.utils import get_unique_username


# Testa se um usuário está sendo criado corretamente
@pytest.mark.django_db
def test_user_creation(cleanup_media_and_users):
    user, data = create_user()

    # Validações
    assert user.id is not None  # Garante que foi salvo no banco
    assert user.email == data["email"]
    assert user.name == data["name"]
    assert user.username == f"@{data['name'].lower().replace(' ', '_')}"
    assert user.check_password(data["password"])


# Testa se o erro para senha inválida está sendo disparado corretamente
@pytest.mark.django_db
def test_user_creation_error_password(cleanup_media_and_users):
    data_error_password = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "password",  # Falta uma letra maiúscula e um número
    }

    serializer = UserCreateSerializer(data=data_error_password)

    assert not serializer.is_valid(), serializer.errors
    assert "password" in serializer.errors
    assert any(
        "A senha deve conter pelo menos uma letra minúscula, uma letra maiúscula e um número."
        in error for error in serializer.errors["password"]
    )


# Testa se o erro para email já em uso está sendo disparado
@pytest.mark.django_db
def test_user_creation_error_email_already_in_use(cleanup_media_and_users):
    _, data = create_user()

    serializer = UserCreateSerializer(data=data)

    assert not serializer.is_valid(), serializer.errors
    assert "email" in serializer.errors

    assert "Já existe um usuário com este e-mail." in serializer.errors["email"][0]


# Testa se o erro para email com formato inválido está sendo disparado
@pytest.mark.django_db
def test_user_creation_error_email_invalid_format():
    invalid_data = {
        "email": "invalid-email",  # Email inválido
        "name": "Test User",
        "password": "Password123",
    }

    serializer = UserCreateSerializer(data=invalid_data)

    assert not serializer.is_valid(), serializer.errors
    assert "email" in serializer.errors
    assert any("Insira um endereço de email válido." in error for error in serializer.errors["email"])
