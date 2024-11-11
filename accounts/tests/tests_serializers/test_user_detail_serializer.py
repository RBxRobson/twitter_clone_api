import pytest
from accounts.models import Profile
from accounts.serializers import UserDetailSerializer
from accounts.factories import UserFactory

@pytest.mark.django_db
def test_user_detail_serializer():
    user = UserFactory()
    Profile.objects.create(user=user)

    serializer = UserDetailSerializer(user)
    data = serializer.data

    assert data["id"] == user.id
    assert data["username"] == user.username
    assert data["name"] == user.name
    assert data["email"] == user.email
    assert data["profile"]["bio"] == ""
    assert data["profile"]["avatar"] == "/media/placeholders/avatar_placeholder.png"
    assert data["profile"]["header"] == "/media/placeholders/header_placeholder.png"
