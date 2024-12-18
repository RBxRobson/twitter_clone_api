from posting.factories import PostFactory, CommentFactory, LikeFactory
from posting.models import Comment, Post
from core.utils import create_user

"""
    Função para testes para criar uma postagem
""" 
def create_post():
    # Cria o usuário para o teste
    user, _ = create_user()

    # Cria um post salvo no banco de dados usando a factory
    post = PostFactory.create(user=user, post_type="original")
    
    return post, user

"""
    Função para testes para criar um comentário
""" 
def create_comment():
    post, user = create_post()
    
    comment = CommentFactory.create(user=user, post=post)
    
    return comment, user

"""
    Função para testes para criar um comentário de resposta
""" 
def create_reply_comment():
    post, user = create_post()
    
    comment = CommentFactory.create(user=user, post=post)
    reply = CommentFactory.create(user=user, post=post, parent_comment=comment)
    
    return reply, comment

"""
    Função para testes para criar um like
""" 
def create_like(arg: Comment | Post):
    # Cria o usuário para o teste
    user, _ = create_user()

    # Verifica se o argumento é uma instância de Comment
    if isinstance(arg, Comment):  
        like = LikeFactory.create(user=user, comment=arg, post=None)
    # Se não for, será uma instância de Post
    else:  
        like = LikeFactory.create(user=user, post=arg, comment=None)

    return like