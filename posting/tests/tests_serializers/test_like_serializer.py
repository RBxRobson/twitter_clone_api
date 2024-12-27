import pytest
from posting.models import Like
from posting.serializers import LikeSerializer
from posting.utils import create_post, create_like, create_comment, create_reply_comment


# Testa se um like em uma postagem está sendo criado corretamente
@pytest.mark.django_db
def test_like_post_creation():
    # Cria uma postagem
    post, _ = create_post()

    # Cria o like na postagem
    like = create_like(arg=post)

    # Instancia o serializer
    serializer = LikeSerializer(like)

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["user"] == like.user.id
    assert serializer.data["post"] == like.post.id

    # Verificação da existência no banco de dados
    assert Like.objects.filter(id=like.id).exists()


# Testa se um like em um comentário está sendo criado corretamente
@pytest.mark.django_db
def test_like_comment_creation():
    # Cria um comentário
    comment, _ = create_comment()

    # Cria o like no comentário
    like = create_like(arg=comment)

    # Instancia o serializer
    serializer = LikeSerializer(like)

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["user"] == like.user.id
    assert serializer.data["comment"] == like.comment.id

    # Verificação da existência no banco de dados
    assert Like.objects.filter(id=like.id).exists()


# Testa se um like em um comentário resposta está sendo criado corretamente
@pytest.mark.django_db
def test_like_reply_creation():
    # Cria um comentário resposta
    reply, _ = create_reply_comment()

    # Cria o like no comentário resposta
    like = create_like(arg=reply)

    # Instancia o serializer
    serializer = LikeSerializer(like)

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["user"] == like.user.id
    assert serializer.data["comment"] == like.comment.id

    # Verificação da existência no banco de dados
    assert Like.objects.filter(id=like.id).exists()
