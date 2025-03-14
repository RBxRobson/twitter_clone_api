import unicodedata
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from accounts.models import User


def get_unique_username(name):
    """
    Gera um nome de usuário único baseado no nome fornecido.
    Remove acentos e substitui espaços por underlines.
    Caso o nome gerado já exista, adiciona um sufixo numérico para garantir a unicidade.
    """
    if not name:
        raise ValueError("O nome não pode ser vazio.")

    # Remove acentos do nome
    name_no_accents = ''.join(
        c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn'
    )

    # Cria o username base, removendo caracteres especiais e garantindo que inicie com '@'
    base_username = f"@{name_no_accents.lower().replace(' ', '_')}"
    username = base_username
    count = 1

    # Verifica se o username já existe no banco, se sim, adiciona um número
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{count}"
        count += 1

    return username


def create_image(name="test_image.jpg", size=(100, 100), color=(73, 109, 137), format="JPEG"):
    """
    Gera uma imagem de teste para campos ImageField.

    Parâmetros:
        - name: Nome do arquivo (padrão: 'test_image.jpg')
        - size: Tamanho da imagem (padrão: (100, 100))
        - color: Cor da imagem no formato RGB (padrão: (73, 109, 137))
        - format: Formato da imagem (padrão: 'JPEG')

    Retorna:
        - SimpleUploadedFile pronto para ser usado em testes.
    """
    image = Image.new("RGB", size, color)
    img_byte_arr = BytesIO()
    image.save
