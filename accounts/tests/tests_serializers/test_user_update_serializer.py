import pytest
from accounts.serializers import UserUpdateSerializer
from accounts.utils import create_image
from core.utils import create_user

# Função para disparar a atualização de apenas um campo
def update_user_unique_key(key: str, value: str, assertion=None, profile=False):
    user, _ = create_user()

    # Define o valor esperado para o teste
    expected_value = assertion if assertion is not None else value

    # Prepara os dados para atualização
    if profile:
        update_data = {"profile": {key: value}}
    else:
        update_data = {key: value}

    # Atualiza o usuário com o serializer
    serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)

    # Verifica se o serializer é válido
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    user.refresh_from_db()
    # Obtém o valor atualizado do usuário ou do perfil
    if profile:
        updated_value = getattr(user.profile, key)
    else:
        updated_value = getattr(user, key)

    # Verifica se o valor foi atualizado corretamente
    assert (
        updated_value == expected_value
    ), f"A chave: {key} deveria ter o valor: {expected_value}, mas seu retorno foi: {updated_value}"

    return True


# Testa atualização parcial das chaves de user e profile
@pytest.mark.django_db
def test_user_update_serializer_update_unique_keys(cleanup_media_and_users):
    # Testa atualização do nome
    update_user_unique_key(key="name", value="Test User Update")

    # Testa atualização do username (deve ter o '@' adicionado)
    update_user_unique_key(
        key="username", value="test_username_10", assertion="@test_username_10"
    )

    # Testa atualização do email
    update_user_unique_key(key="email", value="testuseremail@gmail.com")

    # Testa atualização da bio
    update_user_unique_key(
        profile=True,
        key="bio",
        value="Bio do Test User",
    )


# Testa atualização parcial dos campos ImageField do perfil
@pytest.mark.django_db
def test_user_update_serializer_image_fields(cleanup_media_and_users):
    user, data = create_user()

    # Cria uma imagem válida para os campos avatar e header
    avatar_file = create_image()

    # Atualiza o campo avatar
    update_data = {"profile": {"avatar": avatar_file}}
    serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    user.refresh_from_db()
    assert user.profile.avatar.name.endswith(
        update_data["profile"]["avatar"].name
    ), f"O campo avatar deveria conter o arquivo 'test_image.jpg', mas é '{user.profile.avatar.name}'"

    # Cria uma imagem válida para o campo header
    header_file = create_image()

    # Atualiza o campo header
    update_data = {"profile": {"header": header_file}}
    serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    user.refresh_from_db()
    assert user.profile.header.name.endswith(
        update_data["profile"]["header"].name
    ), f"O campo header deveria conter o arquivo 'test_image.jpg', mas é '{user.profile.header.name}'"


# Testa atualização parcial da senha
@pytest.mark.django_db
def test_user_update_serializer_update_password(cleanup_media_and_users):
    user, _ = create_user()

    # Tentando atualizar a senha
    update_data = {"old_password": "Password123", "password": "Password321"}
    serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)

    # Verifica se o serializer é valido e salva
    assert serializer.is_valid()
    serializer.save()

    user.refresh_from_db()
    # Verifica se atualizou a senha corretamente
    assert user.check_password(update_data["password"])


# Testa atualização completa dos dados de um usuário
@pytest.mark.django_db
def test_user_update_serializer_complete_update(cleanup_media_and_users):
    user, _ = create_user()

    # Cria uma imagem válida para os campo avatar e header
    image = create_image()

    # Tentando atualizar todos os dados de um usuário
    update_data = {
        "name": "Test User Update",
        "email": "test@gmail.com",
        "username": "test_user_10",
        "old_password": "Password123",
        "password": "Password321",
        "profile": {"bio": "Bio Test User", "avatar": image, "header": image},
    }
    serializer = UserUpdateSerializer(instance=user, data=update_data, partial=True)

    # Verifica se o serializer é valido e salva
    assert serializer.is_valid()
    serializer.save()

    user.refresh_from_db()
    # Verifica se atualizou os dados corretamente
    assert user.name == update_data["name"]
    assert user.email == update_data["email"]
    assert user.username == f'@{update_data["username"]}'  # Verifica o '@' prefixo
    assert user.check_password(update_data["password"])
    assert user.profile.bio == update_data["profile"]["bio"]
    assert user.profile.avatar.name.endswith(update_data["profile"]["avatar"].name)
    assert user.profile.header.name.endswith(update_data["profile"]["header"].name)
