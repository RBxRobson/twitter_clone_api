import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User, Profile

@pytest.fixture
def create_user():
    """Fixture para criar um usuário com profile de teste."""
    user = User.objects.create_user(
        name='Test User',
        email='test@example.com',
        password='Password123',
    )
    # Crie um profile associado ao usuário
    profile = Profile.objects.create(user=user, bio="Test Bio")
    return user

@pytest.fixture
def api_client():
    """Fixture para instanciar o APIClient."""
    return APIClient()

@pytest.mark.django_db
def test_create_user(api_client):
    url = reverse('user-list')  # Usando a URL do viewset
    data = {
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'Password123',
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'email' in response.data  # Verifique se o email foi retornado
    assert response.data['email'] == 'newuser@example.com'

@pytest.mark.django_db
def test_list_users(api_client, create_user):
    url = reverse('user-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  # Verifica se pelo menos um usuário foi retornado

@pytest.mark.django_db
def test_retrieve_user(api_client, create_user):
    url = reverse('user-detail', args=[create_user.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == create_user.email

@pytest.mark.django_db
def test_update_user(api_client, create_user):
    url = reverse('user-detail', args=[create_user.id])
    data = {
        'name': 'Updated User',
        'email': 'updated@example.com',
        'password': 'NewPassword123',
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    updated_user = User.objects.get(id=create_user.id)
    assert updated_user.name == 'Updated User'
    assert updated_user.email == 'updated@example.com'

@pytest.mark.django_db
def test_partial_update_user(api_client, create_user):
    url = reverse('user-detail', args=[create_user.id])
    data = {
        'name': 'Partially Updated User',
    }

    response = api_client.patch(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    updated_user = User.objects.get(id=create_user.id)
    assert updated_user.name == 'Partially Updated User'
