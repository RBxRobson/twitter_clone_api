import pytest
from rest_framework.test import APIRequestFactory
from accounts.serializers import UserDetailSerializer
from core.utils import create_user


@pytest.mark.django_db
def test_user_detail_serializer(cleanup_media_and_users):
    user, _ = create_user()

    # Simulando uma requisição para passar no contexto do serializer
    factory = APIRequestFactory()
    request = factory.get("/")
    request.user = user  # Definir o usuário autenticado na requisição

    # Chamando o serializer com o usuário autenticado
    serializer = UserDetailSerializer(user, context={"request": request})
    data_serializer = serializer.data

    # Validações
    assert data_serializer["id"] == user.id
    assert data_serializer["username"] == user.username
    assert data_serializer["name"] == user.name
    assert data_serializer["email"] == user.email
    assert data_serializer["profile"]["bio"] == user.profile.bio
    assert data_serializer["profile"]["avatar"] == user.profile.avatar.url
    assert data_serializer["profile"]["header"] == user.profile.header.url
    assert data_serializer["followers_count"] == user.followers.count()
    assert data_serializer["following_count"] == user.following.count()

    # O campo is_following NÃO deve aparecer quando o próprio usuário está autenticado
    assert "is_following" not in data_serializer

@pytest.mark.django_db
def test_user_detail_serializer_with_other_user(cleanup_media_and_users):
    user, _ = create_user()
    other_user, _ = create_user()

    # Simulando uma requisição onde outro usuário está autenticado
    factory = APIRequestFactory()
    request = factory.get("/")
    request.user = other_user  # Autenticando outro usuário na requisição

    # Chamando o serializer com o usuário autenticado diferente do serializado
    serializer = UserDetailSerializer(user, context={"request": request})
    data_serializer = serializer.data

    # O campo is_following deve aparecer e ser um booleano
    assert "is_following" in data_serializer
    assert isinstance(data_serializer["is_following"], bool)
