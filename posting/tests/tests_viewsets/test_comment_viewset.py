import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from posting.utils import create_post, create_comment
from core.utils import perform_login


# Fixture para instanciar o APIClient
@pytest.fixture
def api_client():
    return APIClient()


# Testa se é possível comentar em uma postagem
@pytest.mark.django_db
def test_comment_post(api_client):
    # Cria a postagem para o teste
    post, user = create_post()

    # Faz login do usuário e salva o token de acesso
    token_access = perform_login(api_client, email=user.email, password="Password123")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_access}")

    # Dados do comentário
    comment_data = {"content": "Este é um comentário de teste."}

    # URL do endpoint de comentários
    url = reverse("post-comments-list", kwargs={"post_pk": post.id})

    # Faz a requisição POST para criar o comentário
    response = api_client.post(url, comment_data, format="json")

    # Verificações do teste
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["content"] == comment_data["content"]
    assert response.data["post"] == post.id


# Testa se é possível responder um comentário em uma postagem
@pytest.mark.django_db
def test_reply_comment_post(api_client):
    # Cria o comentário para o teste
    comment, user = create_comment()

    # Faz login do usuário e salva o token de acesso
    token_access = perform_login(api_client, email=user.email, password="Password123")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_access}")

    # Dados do comentário resposta
    reply_data = {
        "parent_comment": comment.id,
        "content": "Este é um comentário de resposta teste.",
    }

    # URL do endpoint de comentários resposta
    url = reverse(
        "post-comments-replies", kwargs={"post_pk": comment.post.id, "pk": comment.id}
    )

    # Faz a requisição POST para criar a resposta
    response = api_client.post(url, reply_data, format="json")

    # Verificações do teste
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["content"] == reply_data["content"]
    assert response.data["post"] == comment.post.id
