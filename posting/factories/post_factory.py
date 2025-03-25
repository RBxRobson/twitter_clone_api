import factory
from faker import Faker
from posting.models import Post

faker = Faker()

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory("core.factories.UserFactory")
    content = factory.LazyAttribute(lambda o: "" if o.post_type == Post.REPOST else faker.text(max_nb_chars=280))
    post_type = Post.ORIGINAL
    original_post = None
