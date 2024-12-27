import factory
from factory.django import DjangoModelFactory
from accounts.factories import UserFactory
from posting.factories import PostFactory, CommentFactory
from posting.models import Like


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    comment = factory.SubFactory(CommentFactory)
