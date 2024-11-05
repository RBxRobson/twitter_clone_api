import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from accounts.factories import UserFactory

@pytest.mark.django_db
class TestUserViewSet:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client

    # Testa a criação de um usuário pela API.
    def test_create_user(self, api_client):
        url = reverse('user-list')
        data = {
            "name": "New User",
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password123"
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(username="@newuser").exists()

    # Testa a recuperação dos dados de um usuário autenticado.
    def test_retrieve_user(self, auth_client, user):
        url = reverse('user-detail', args=[user.id])
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.data["username"] == user.username

    # Testa a atualização dos dados de um usuário.
    def test_update_user(self, auth_client, user):
        url = reverse('user-detail', args=[user.id])
        data = {"name": "Updated Name"}
        response = auth_client.patch(url, data, format='json')
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.name == "Updated Name"

    # Testa a exclusão de um usuário.
    def test_delete_user(self, auth_client, user):
        url = reverse('user-detail', args=[user.id])
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert not User.objects.filter(id=user.id).exists()

    # Testa a criação de um usuário não autenticado.
    def test_create_user_unauthenticated(self, api_client):
        url = reverse('user-list')
        data = {
            "name": "Another User",
            "username": "anotheruser",
            "email": "anotheruser@example.com",
            "password": "Password123"
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201  # Verifica que o usuário foi criado

    # Testa a tentativa de atualização de um usuário sem autenticação.
    def test_update_user_unauthenticated(self, api_client, user):
        url = reverse('user-detail', args=[user.id])
        data = {"name": "Attempted Update"}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == 403  # Verifica que a atualização foi negada

    # Testa a tentativa de deleção de um usuário sem autenticação.
    def test_delete_user_unauthenticated(self, api_client, user):
        url = reverse('user-detail', args=[user.id])
        response = api_client.delete(url)
        assert response.status_code == 403  # Verifica que a deleção foi negada

    # Testa a recuperação de um usuário que não existe.
    def test_retrieve_non_existent_user(self, auth_client):
        url = reverse('user-detail', args=[9999])  # ID de um usuário que não existe
        response = auth_client.get(url)
        assert response.status_code == 404  # Verifica que o usuário não foi encontrado

