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

    # Define o conteúdo condicionalmente com base no post_type
    @factory.lazy_attribute
    def content(self):
        if self.post_type == Post.REPOST:
            return ""
        else: 
            return factory.Faker('text', max_nb_chars=280).evaluate(None, None, {'locale': None})

    @factory.post_generation
    # Define um post original ao criar reposts ou quotes.
    def original_post(self, create, extracted, **kwargs):
        if not create:
            return

        if self.post_type in {Post.REPOST, Post.QUOTE}:
            if extracted:
                # Use o post fornecido
                self.original_post = extracted
            else:
                # Cria um novo post original caso nenhum tenha sido fornecido
                self.original_post = PostFactory(post_type=Post.ORIGINAL)
            self.save()