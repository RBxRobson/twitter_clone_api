import pytest
from accounts.serializers import UserCreateSerializer
from core.utils import create_user

# Testa se um usuário está sendo criado corretamente
@pytest.mark.django_db
def test_user_creation(cleanup_media_and_users):
    user, data = create_user()

    # Validações
    assert user.email == data["email"]
    assert user.name == data["name"]
    assert user.username is not None and user.username != ""
    assert user.username == f"@{data['name'].lower().replace(' ', '_')}"
    assert user.check_password(data["password"]) 

# Testa se o erro para senha está sendo disparado
@pytest.mark.django_db
def test_user_creation_error_password(cleanup_media_and_users):
    data_error_password = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "password"  # Falta uma letra maiúscula e algum número
    }

    # Instanciando o serializer
    serializer = UserCreateSerializer(data=data_error_password)

    # Certifique-se de que os dados NÃO são válidos
    assert not serializer.is_valid(), serializer.errors  

    # Verifica se o erro esperado foi gerado para a senha
    assert 'password' in serializer.errors
    assert 'A senha deve conter pelo menos uma letra minúscula, uma letra maiúscula e um número.' in serializer.errors['password'][0]

# Testa se o erro para email já em uso está sendo disparado
@pytest.mark.django_db
def test_user_creation_error_email_already_in_use(cleanup_media_and_users):
    # Cria um usuário
    _, data = create_user()

    # Agora, tenta criar um segundo usuário com o mesmo email
    serializer = UserCreateSerializer(data=data)

    # Certifique-se de que os dados NÃO são válidos
    assert not serializer.is_valid(), serializer.errors

    # Verifica se o erro de email já em uso foi gerado
    assert 'email' in serializer.errors
    assert 'user with this email already exists.' in serializer.errors['email'][0]

# Testa se o erro para email com formato inválido está sendo disparado
@pytest.mark.django_db
def test_user_creation_error_email_invalid_format():
    # Dados com email inválido
    invalid_data = {
        "email": "invalid-email",  # Email inválido
        "name": "Test User",
        "password": "password123"
    }

    # Instanciando o serializer com o email inválido
    serializer = UserCreateSerializer(data=invalid_data)

    # Certifique-se de que os dados NÃO são válidos
    assert not serializer.is_valid(), serializer.errors

    # Verifica se o erro de formato de email foi gerado
    assert 'email' in serializer.errors
    assert 'Enter a valid email address.' in serializer.errors['email'][0]

