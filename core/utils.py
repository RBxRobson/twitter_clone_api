from rest_framework import status
from django.urls import reverse
from accounts.factories import UserFactory

"""
    Função para testes para criar um usuário 
"""


def create_user():
    from accounts.serializers import UserCreateSerializer

    # Usando a fábrica para criar um usuário
    user = UserFactory.build()
    data = {
        "email": user.email,
        "name": user.name,
        "password": "Password123",
    }

    # Serializando o usuário com o UserCreateSerializer
    serializer = UserCreateSerializer(data=data)

    # Certifique-se de que os dados são válidos
    assert serializer.is_valid(), serializer.errors

    # Salvando o usuário
    user = serializer.save()

    return user, data


"""
    Função para testes para logar usuário
"""


def perform_login(api_client, email, password):
    login_url = reverse("login")
    login_data = {"email": email, "password": password}
    response = api_client.post(login_url, data=login_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    return response.data["access"]
