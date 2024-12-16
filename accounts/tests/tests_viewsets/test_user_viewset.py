import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from core.utils import perform_login, create_user

def follow_user(api_client, user_id):
    follow_url = reverse('user-follow', args=[user_id])
    response = api_client.post(follow_url, format='json')
    assert response.status_code == status.HTTP_200_OK
    return response

def unfollow_user(api_client, user_id):
    unfollow_url = reverse('user-unfollow', args=[user_id])
    response = api_client.post(unfollow_url, format='json')
    assert response.status_code == status.HTTP_200_OK
    return response

@pytest.fixture
def api_client():
    """Fixture para instanciar o APIClient."""
    return APIClient()

# Verifica criação de usuários
@pytest.mark.django_db
def test_create_user(api_client, cleanup_media_and_users):
    url = reverse('user-list')  # Usando a URL do viewset
    data = {
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'Password123',
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == data['email']

# Verifica listagem de usuários
@pytest.mark.django_db
def test_list_users(api_client, cleanup_media_and_users):
    create_user()
    url = reverse('user-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    # Verifica se pelo menos um usuário foi retornado
    assert len(response.data) > 0 

# Verifica retorno de usuário pelo id
@pytest.mark.django_db
def test_retrieve_user(api_client):
    user, data = create_user()
    url = reverse('user-detail', args=[user.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user.email

# Verifica atualização de usuário
@pytest.mark.django_db
def test_update_user(api_client, cleanup_media_and_users):
    user, data = create_user()
    
    url = reverse('user-detail', args=[user.id])
    updated_data = {
        'name': 'Updated User',
        'email': 'updated@example.com',
        'old_password': data["password"],
        'password': 'NewPassword123'
    }

    response = api_client.put(url, updated_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    updated_user = User.objects.get(id=user.id)
    assert updated_user.name == updated_data['name']
    assert updated_user.email == updated_data['email']

# Verifica se é possível seguir/deixar de seguir um usuário
@pytest.mark.django_db
def test_follow_and_unfollowing_user(api_client, cleanup_media_and_users):
    # Cria dois usuários
    user1, data_user1 = create_user()
    user2, _ = create_user()

    # Realiza login com o primeiro usuário
    token_access = perform_login(api_client, user1.email, data_user1["password"])
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_access}')

    # Seguir o usuário
    follow_response = follow_user(api_client, user2.id)
    assert follow_response.data['detail'] == f"Você agora está seguindo {user2.username}."

    # Verifica relacionamentos
    user1.refresh_from_db()
    assert user2 in user1.following.all()

    # Deixar de seguir o usuário
    unfollow_response = unfollow_user(api_client, user2.id)
    assert unfollow_response.data['detail'] == f"Você deixou de seguir {user2.username}."

    # Verifica relacionamentos novamente
    user1.refresh_from_db()
    assert user2 not in user1.following.all()

# Verifica o retorno da lista de seguidores e seguindo
@pytest.mark.django_db
def test_following_and_folllowers_list(api_client, cleanup_media_and_users):
    # Cria dois usuários
    user1, data_user1 = create_user()
    user2, _ = create_user()

    # Realiza login com o usuário 1
    token_access = perform_login(api_client, user1.email, data_user1["password"])
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_access}')

    # Segue o usuário 2 com o usuário 1
    follow_user(api_client, user2.id)

    # Acessa lista de seguindo do usuário 1
    url_following = reverse('user-following', args=[user1.id])
    response_following = api_client.get(url_following, format='json')

    # Verifica se tem o retorno da lista de seguindo é igual a 1
    assert response_following.status_code == status.HTTP_200_OK
    assert len(response_following.json()) == 1

    # Acessa lista de seguidores do usuário 2
    url_followers = reverse('user-followers', args=[user2.id])
    response_followers = api_client.get(url_followers, format='json')

    # Verifica se tem o retorno da lista de seguidores é igual a 1
    assert response_followers.status_code == status.HTTP_200_OK
    assert len(response_followers.json()) == 1