import factory
from factory.django import DjangoModelFactory
from accounts.factories import UserFactory
from posting.factories import PostFactory
from posting.models import Comment

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker('text', max_nb_chars=280)
    parent_comment = None