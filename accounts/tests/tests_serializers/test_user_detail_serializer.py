import pytest
from accounts.serializers import UserDetailSerializer
from accounts.utils import create_user

@pytest.mark.django_db
def test_user_detail_serializer(cleanup_media_and_users):
    user, _ = create_user()

    # Chamando o serializer de busca com o user criado antes
    serializer = UserDetailSerializer(user)
    data_serializer = serializer.data

    # Validações
    assert data_serializer["id"] == user.id
    assert data_serializer["username"] == user.username
    assert data_serializer["name"] == user.name
    assert data_serializer["email"] == user.email
    assert data_serializer["profile"]["bio"] == user.profile.bio
    assert data_serializer["profile"]["avatar"] == f'/media/{user.profile.avatar.name}'
    assert data_serializer["profile"]["header"] == f'/media/{user.profile.header.name}'

