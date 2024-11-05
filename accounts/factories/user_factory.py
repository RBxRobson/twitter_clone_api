import factory
from accounts.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Gera valores padrão para os campos
    name = factory.Faker('name')
    email = factory.Faker('email')

    # Gera uma senha padrão e um username respeitando as exigência
    password = factory.LazyFunction(lambda: make_password('Password123'))
    username = factory.LazyAttribute(lambda obj: f'@{obj.name.lower().replace(" ", "_")}')

    # Define se o usuário está ativo
    is_active = True
