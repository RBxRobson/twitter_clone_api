import factory
from accounts.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password('Password123'))
    is_active = True

    # Override para salvar após a criação dos campos gerados
    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        obj.save()
