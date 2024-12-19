import pytest
from posting.models import Post
from posting.factories import PostFactory
from posting.serializers import PostSerializer
from posting.utils import create_post

# Testa se uma postagem original está sendo criada corretamente
@pytest.mark.django_db
def test_post_original_creation():
    post, user = create_post()

    # Instancia o serializer passando os dados do post
    serializer = PostSerializer(post)  

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["post_type"] == Post.ORIGINAL
    assert serializer.data["user"] == user.id
    assert serializer.data["content"] == post.content

    # Verificação da existência no banco de dados
    assert Post.objects.filter(id=post.id).exists()

# Testa se uma repostagem está sendo criada corretamente
@pytest.mark.django_db
def test_post_repost_creation():
    post, user = create_post()

    # Cria um repost usando o post original criado anteriormente
    repost = PostFactory.create(user=user, post_type=Post.REPOST, original_post=post)

    # Instancia o serializer passando os dados do post
    serializer = PostSerializer(repost)  

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["post_type"] == Post.REPOST
    assert serializer.data["user"] == user.id
    assert serializer.data["content"] == ""

    # Verificação da existência no banco de dados
    assert Post.objects.filter(id=repost.id).exists()

# Testa se uma citação está sendo criada corretamente
@pytest.mark.django_db
def test_post_quote_creation():
    post, user = create_post()

    # Cria uma citação usando o post original criado anteriormente
    quote = PostFactory.create(user=user, post_type=Post.QUOTE, original_post=post)

    # Instancia o serializer passando os dados do post
    serializer = PostSerializer(quote)  

    # Verifica os dados serializados
    assert serializer.data
    assert serializer.data["post_type"] == Post.QUOTE
    assert serializer.data["user"] == user.id
    assert serializer.data["content"] == quote.content

    # Verificação da existência no banco de dados
    assert Post.objects.filter(id=quote.id).exists()