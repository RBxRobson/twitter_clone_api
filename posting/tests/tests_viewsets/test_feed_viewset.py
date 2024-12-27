import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from posting.utils import create_post
from core.utils import perform_login, create_user


# Fixture para instanciar o APIClient
@pytest.fixture
def api_client():
    return APIClient()


# Testa se o retorno do feed está correto
@pytest.mark.django_db
def test_like_post(api_client):
    # Cria a postagem para o teste
    post, user1 = create_post()
    user, _ = create_user()

    # Faz login do usuário e salva o token de acesso
    token_access = perform_login(api_client, email=user.email, password="Password123")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_access}")

    # Segue o usuário da postagem
    follow_url = reverse("user-follow", args=[user1.id])
    response_follow = api_client.post(follow_url, format="json")
    assert response_follow.status_code == status.HTTP_200_OK
    assert (
        response_follow.data["detail"] == f"Você agora está seguindo {user1.username}."
    )

    # Usando a URL do viewset
    url = reverse("feed-list")

    # Faz a requisição e salva a sua resposta
    response = api_client.get(url)

    # Verificações do teste
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["user_details"]["id"] == user1.id
