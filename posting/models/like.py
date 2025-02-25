from django.db import models
from accounts.models import User
from .post import Post


class Like(models.Model):
    # O usuário que deu o like
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    # O post que recebeu o like (inclui posts, reposts, quotes e comentários)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    # Campos de tracking
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que o usuário só possa curtir um post (ou comentário) uma única vez
        unique_together = ("user", "post")

    def __str__(self):
        return f"Like de {self.user.username} no post {self.post.id}"
