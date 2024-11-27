from django.db import models
from accounts.models import User
from .post import Post
from .comment import Comment

class Like(models.Model):
    # O usuário que deu o like
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    # Relacionamento com Post ou Comment (não ambos ao mesmo tempo)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name="likes")
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE, related_name="likes")

    # Campos de tracking
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que o usuário só possa curtir uma vez o mesmo post ou comentário
        unique_together = ('user', 'post')
        unique_together = ('user', 'comment')

    def __str__(self):
        if self.post:
            return f"Like de {self.user.username} no post {self.post.id}"
        else:
            return f"Like de {self.user.username} no comentário {self.comment.id}"
