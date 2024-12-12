from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from accounts.models import User
from accounts.factories import UserFactory

"""
    Gera um nome de usuário único baseado no nome fornecido.
    Caso o nome gerado já exista, adiciona 
    um sufixo numérico para garantir a unicidade.
"""
def get_unique_username(name):
    base_username = f"@{name.lower().replace(' ', '_')}"
    username = base_username
    count = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{count}"
        count += 1

    return username

"""
    Cria um usuário para testes
"""
def create_user():
    from accounts.serializers import UserCreateSerializer
    # Usando a fábrica para criar um usuário
    user = UserFactory.build()
    data = {
        'email': user.email,
        'name': user.name,
        'password': 'Password123',
    }

    # Serializando o usuário com o UserCreateSerializer
    serializer = UserCreateSerializer(data=data)

    # Certifique-se de que os dados são válidos
    assert serializer.is_valid(), serializer.errors

    # Salvando o usuário
    user = serializer.save()

    return user, data

"""
    Função para gerar uma imagem para testes de campos ImageField
"""
def create_image():
    image = Image.new('RGB', (100, 100), color=(73, 109, 137))
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_byte_arr.read(), content_type="image/jpeg")