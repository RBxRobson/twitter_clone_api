from posting.factories import PostFactory, LikeFactory
from posting.models import Post
from core.utils import create_user

"""
    Função para testes para criar uma postagem
"""
def create_post():
    # Cria o usuário para o teste
    user, _ = create_user()

    # Cria um post salvo no banco de dados usando a factory
    post = PostFactory.create(user=user, post_type=Post.ORIGINAL)

    return post, user


"""
    Função para testes para criar um comentário
"""
def create_comment():
    post_original, user = create_post()

    # Cria um comentário salvo no banco de dados usando a factory
    comment = PostFactory.create(user=user, post_type=Post.COMMENT, original_post=post_original)

    return comment, user


"""
    Função para testes para criar um comentário de resposta
"""
def create_reply_comment():
    post, user = create_post()

    # Cria um comentário em um post
    comment = PostFactory.create(user=user, post_type=Post.COMMENT, original_post=post)

    # Cria uma resposta para o comentário
    reply = PostFactory.create(user=user, post_type=Post.COMMENT, original_post=comment)

    return reply, user, comment


"""
    Função para testes para criar um like
"""
def create_like(post: Post, user=None):
    if user is None:
        user, _ = create_user()
    
    like = LikeFactory.create(user=user, post=post)
    return like
