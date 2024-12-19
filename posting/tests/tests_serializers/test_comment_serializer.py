import pytest
from posting.models import Comment
from posting.serializers import CommentSerializer
from posting.utils import create_comment, create_reply_comment

# Testa se um comentário está sendo criado corretamente
@pytest.mark.django_db
def test_comment_creation():
    comment, user = create_comment()

    serializer = CommentSerializer(comment)

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["user"] == user.id
    assert serializer.data["post"] == comment.post.id
    assert serializer.data["content"] == comment.content

    # Verificação da existência no banco de dados
    assert Comment.objects.filter(id=comment.id).exists()

# Testa se um comentário resposta está sendo criado corretamente
@pytest.mark.django_db
def test_reply_creation():
    reply, comment = create_reply_comment()

    serializer = CommentSerializer(reply)

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["user"] == reply.user.id
    assert serializer.data["parent_comment"] == comment.id
    assert serializer.data["post"] == comment.post.id
    assert serializer.data["content"] == reply.content

    # Verificação da existência no banco de dados
    assert Comment.objects.filter(id=reply.id).exists()
