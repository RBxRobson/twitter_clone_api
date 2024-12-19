import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from posting.utils import create_post
from core.utils import perform_login, create_user
from posting.models import Post, Like

# Fixture para instanciar o APIClient
@pytest.fixture
def api_client():
    return APIClient()

# Testa a criação de uma postagem original
@pytest.mark.django_db
def test_create_original_post(api_client):
    # Cria o usuário para o teste
    user, data_user = create_user()

    # Data do post enviado
    data_post={
        "post_type": "original",
        "content": f"Postagem original do {user.username}"
    }

    # Faz login do usuário e salva o token de acesso
    token_access = perform_login(api_client, email=user.email, password=data_user["password"])
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_access}') 

    # Usando a URL do viewset
    url = reverse('post-list') 

    # Faz a requisição e salva a sua resposta
    response = api_client.post(url, data_post, format='json')

    # Verificações do teste
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['content'] == data_post['content']
    assert response.data['user'] == user.id

# Testa a atualização de um post
@pytest.mark.django_db
def test_updated_original_post(api_client):
    # Cria a postagem para o teste
    post, user = create_post()

    # Faz login do usuário e salva o token de acesso
    token_access = perform_login(api_client, email=user.email, password="Password123")
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_access}') 

    # Usando a URL do viewset
    url = reverse('post-detail', args=[post.id])

    data = {
        "content": f"Atualização da postagem do {user.username}"
    }

    # Faz a requisição e salva a sua resposta
    response = api_client.put(url, data, format='json')

    # Verificações do teste
    assert response.status_code == status.HTTP_200_OK
    assert response.data['content'] == data['content']
    assert response.data['user'] == user.id

# Testa se uma postagem está sendo deletada corretamente
@pytest.mark.django_db
def test_delete_post(api_client):
    # Cria a postagem para o teste
    post, user = create_post()

    # Faz login do usuário e salva o token de acesso
    token_access = perform_login(api_client, email=user.email, password="Password123")
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_access}') 

    # Usando a URL do viewset
    url = reverse('post-detail', args=[post.id])

    # Faz a requisição e salva a sua resposta
    response = api_client.delete(url, format='json')

    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verifica se a postagem foi deletada do banco de dados
    assert not Post.objects.filter(id=post.id).exists()

# Testa se a listagem de postagens está correta
@pytest.mark.django_db
def test_post_list(api_client):
    # Cria a postagem para o teste
    post, _ = create_post()

    # Usando a URL do viewset
    url = reverse('post-list')

    # Faz a requisição e salva a sua resposta
    response = api_client.get(url)

    # Verificações
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0 
    assert response.data[0]["content"] == post.content

# Testa se o retorno dos detalhes de uma postagem é o esperado
@pytest.mark.django_db
def test_post_detail(api_client):
    # Cria a postagem para o teste
    post, user = create_post()

    # Usando a URL do viewset
    url = reverse('post-detail', args=[post.id])

    # Faz a requisição e salva a sua resposta
    response = api_client.get(url)

    # Verificações
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user_details"]["id"] == user.id
    assert response.data["user_details"]["username"] == user.username
    assert response.data["user_details"]["name"] == user.name
    assert response.data["user_details"]["avatar"] == f'/media/{user.profile.avatar.name}'
    assert response.data["content"] == post.content

# Testa se é possível dar um like em um post
@pytest.mark.django_db
def test_like_post(api_client):
    # Cria a postagem para o teste
    post, user = create_post()

    # Faz login do usuário e salva o token de acesso
    token_access = perform_login(api_client, email=user.email, password="Password123")
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_access}') 

    # Usando a URL do viewset
    url = reverse('post-likes', args=[post.id])

    # Faz a requisição e salva a sua resposta
    response = api_client.post(url, format='json')

    # Verificações do teste
    assert response.status_code == status.HTTP_201_CREATED
    assert Like.objects.filter(id=response.data["id"]).exists()