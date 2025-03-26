import pytest
from rest_framework.test import APIRequestFactory
from posting.models import Post
from posting.factories import PostFactory
from posting.serializers import PostSerializer
from posting.utils import create_post

@pytest.fixture
def api_request_factory():
    return APIRequestFactory()

@pytest.mark.django_db
def test_post_original_creation(api_request_factory):
    post, user = create_post()
    request = api_request_factory.get("/fake-url/")
    request.user = user
    
    serializer = PostSerializer(post, context={"request": request})
    
    assert serializer.data
    assert serializer.data["post_type"] == Post.ORIGINAL
    assert serializer.data["user_details"]["id"] == user.id
    assert serializer.data["content"] == post.content
    assert Post.objects.filter(id=post.id).exists()

@pytest.mark.django_db
def test_post_repost_creation(api_request_factory):
    post, user = create_post()
    repost = PostFactory.create(user=user, post_type=Post.REPOST, original_post=post)
    request = api_request_factory.get("/fake-url/")
    request.user = user
    
    serializer = PostSerializer(repost, context={"request": request})
    
    assert serializer.data
    assert serializer.data["post_type"] == Post.REPOST
    assert serializer.data["user_details"]["id"] == user.id
    assert serializer.data["content"] == ""
    assert Post.objects.filter(id=repost.id).exists()

@pytest.mark.django_db
def test_post_quote_creation(api_request_factory):
    post, user = create_post()
    quote = PostFactory.create(user=user, post_type=Post.QUOTE, original_post=post)
    request = api_request_factory.get("/fake-url/")
    request.user = user
    
    serializer = PostSerializer(quote, context={"request": request})
    
    assert serializer.data
    assert serializer.data["post_type"] == Post.QUOTE
    assert serializer.data["user_details"]["id"] == user.id
    assert serializer.data["content"] == quote.content
    assert Post.objects.filter(id=quote.id).exists()
