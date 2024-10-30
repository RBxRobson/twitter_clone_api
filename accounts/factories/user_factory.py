import factory
from accounts.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Gera valores padrão para os campos
    name = factory.Faker('name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')

    # Gera uma senha padrão, criptografando-a corretamente
    password = factory.LazyFunction(lambda: make_password('Password123'))

    # Define se o usuário está ativo
    is_active = True
