from accounts.models import User

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