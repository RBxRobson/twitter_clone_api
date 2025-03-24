import factory
from factory.django import DjangoModelFactory
from accounts.factories import UserFactory
from posting.factories import PostFactory
from posting.models import Like


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Garante que um usuário não curta o mesmo post mais de uma vez, respeitando a restrição unique_together.
        """
        user = kwargs.get("user") or UserFactory()
        post = kwargs.get("post") or PostFactory()

        if not model_class.objects.filter(user=user, post=post).exists():
            return super()._create(model_class, *args, **kwargs)
        
        return model_class.objects.filter(user=user, post=post).first()