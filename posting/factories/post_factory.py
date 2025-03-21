import factory
from factory.django import DjangoModelFactory
from accounts.factories import UserFactory
from posting.models import Post


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    post_type = factory.Iterator([Post.ORIGINAL, Post.REPOST, Post.QUOTE, Post.COMMENT])
    content = factory.LazyAttribute(lambda obj: factory.Faker("text", max_nb_chars=280).generate({}) if obj.post_type != Post.REPOST else "")

    @factory.post_generation
    def original_post(self, create, extracted, **kwargs):
        if not create:
            return

        if self.post_type in {Post.REPOST, Post.QUOTE, Post.COMMENT}:
            self.original_post = extracted if extracted else PostFactory(post_type=Post.ORIGINAL)
            self.save()