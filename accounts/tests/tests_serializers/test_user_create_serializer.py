import pytest
from accounts.models import User, Profile
from accounts.serializers import UserCreateSerializer

@pytest.mark.django_db
def test_user_create_serializer_valid_data():
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "Password123"
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()

    # Verifica se o usuário foi criado com sucesso e se o perfil está associado
    assert User.objects.filter(email="john.doe@example.com").exists()
    assert Profile.objects.filter(user=user).exists()
    assert user.check_password("Password123")

@pytest.mark.django_db
def test_user_create_serializer_invalid_password():
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password"  # senha inválida, sem maiúscula e número
    }
    serializer = UserCreateSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors
