import unicodedata
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from accounts.models import User

"""
    Gera um nome de usuário único baseado no nome fornecido.
    Caso o nome gerado já exista, adiciona 
    um sufixo numérico para garantir a unicidade.
"""


def get_unique_username(name):
    # Remove acentos do nome
    name_no_accents = ''.join(
        c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn'
    )
    
    # Cria o username base
    base_username = f"@{name_no_accents.lower().replace(' ', '_')}"
    username = base_username
    count = 1

    # Verifica se o username já existe, se sim, adiciona um número
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{count}"
        count += 1

    return username


"""
    Função para gerar uma imagem para testes de campos ImageField
"""


def create_image():
    image = Image.new("RGB", (100, 100), color=(73, 109, 137))
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)
    return SimpleUploadedFile(
        "test_image.jpg", img_byte_arr.read(), content_type="image/jpeg"
    )
