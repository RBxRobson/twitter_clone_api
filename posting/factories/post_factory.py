import factory
from factory.django import DjangoModelFactory
from accounts.factories import UserFactory
from posting.models import Post


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    post_type = Post.ORIGINAL
    content = factory.Maybe(
        "post_type",
        factory.Faker("text", max_nb_chars=280),
        "",  # Se for REPOST, o conteúdo será vazio
    )

    @factory.post_generation
    def original_post(self, create, extracted, **kwargs):
        if not create:
            return

        if self.post_type in {Post.REPOST, Post.QUOTE, Post.COMMENT}:
            if extracted:
                self.original_post = extracted
            else:
                self.original_post = PostFactory(post_type=Post.ORIGINAL)
            self.save()
