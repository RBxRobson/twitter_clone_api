import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from posting.models import Like
from posting.serializers import LikeSerializer
from posting.utils import create_post, create_like

@pytest.fixture
def api_request_factory():
    return APIRequestFactory()

@pytest.mark.django_db
def test_like_post_creation():
    """Testa a criação de um like em uma postagem"""
    post, user = create_post()
    like = create_like(post=post, user=user)

    serializer = LikeSerializer(like)
    
    assert serializer.data
    assert serializer.data["user"] == like.user.id
    assert serializer.data["post"] == like.post.id
    assert Like.objects.filter(id=like.id).exists()

@pytest.mark.django_db
def test_like_post_creation_post_request(api_request_factory):
    """Testa a serialização de um like via requisição POST"""
    post, user = create_post()
    like = create_like(post=post, user=user)

    request = api_request_factory.post("/fake-url/")
    request.user = user
    serializer = LikeSerializer(like, context={"request": request})

    assert serializer.data
    assert "user_details" not in serializer.data  # Deve ser removido no POST

@pytest.mark.django_db
def test_like_validation():
    """Testa a validação de um like sem post"""
    serializer = LikeSerializer(data={})
    assert not serializer.is_valid()
    assert "post" in serializer.errors
    assert str(serializer.errors["post"][0]) == "Este campo é obrigatório."
