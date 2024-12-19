import factory
from accounts.models import User
from faker import Faker

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True


    # Garante que o email será único
    email = factory.LazyAttribute(lambda _: fake.unique.email())  
    name = factory.Faker('name')
    password = factory.PostGenerationMethodCall('set_password', 'Password123')
