import os
import pytest
from django.conf import settings
from accounts.models import User

"""
    Função para limpar as imagens após os testes
"""
@pytest.fixture(scope="function")
def cleanup_media_and_users():
    yield
    # Caminhos para as pastas onde as imagens são salvas
    media_root = settings.MEDIA_ROOT
    avatar_path = os.path.join(media_root, 'avatars', 'test_image.jpg')
    header_path = os.path.join(media_root, 'headers', 'test_image.jpg')

    # Verificar se os arquivos existem e removê-los
    if os.path.exists(avatar_path):
        os.remove(avatar_path)

    if os.path.exists(header_path):
        os.remove(header_path)

    # Limpa todos os usuários no final de cada teste
    User.objects.all().delete() 