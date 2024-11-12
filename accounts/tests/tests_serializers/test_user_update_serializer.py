import pytest
from accounts.serializers import UserCreateSerializer, UserUpdateSerializer
from accounts.factories import UserFactory
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_update_serializer_update_name():
    # Criando e salvando o usuário diretamente com UserFactory
    user = UserFactory.create()

    # Atualizando o nome do usuário com UserUpdateSerializer
    update_data = {"name": "Jane Updated"}
    update_serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)
    assert update_serializer.is_valid()
    update_serializer.save()

    user.refresh_from_db()
    assert user.name == "Jane Updated"

@pytest.mark.django_db
def test_user_update_serializer_invalid_username():
    user = UserFactory.create()

    # Tentando atualizar com um username inválido
    update_data = {"username": "invalid username!"}
    update_serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)
    assert not update_serializer.is_valid()
    assert "username" in update_serializer.errors

@pytest.mark.django_db
def test_user_update_serializer_update_password():
    user = UserFactory.create()

    # Atualizando a senha do usuário com UserUpdateSerializer
    update_data = {"password": "NewPassword123"}
    update_serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)
    assert update_serializer.is_valid()
    update_serializer.save()

    user.refresh_from_db()
    assert user.check_password("NewPassword123")
