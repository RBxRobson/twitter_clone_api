from django.db import models
from accounts.models import User
from .post import Post

class Comment(models.Model):
    # Usuário que fez o comentário
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    
    # Conteúdo do comentário
    content = models.TextField(max_length=280)

    # Relacionamento com um Post (se o comentário é feito diretamente em um Post)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name="comments")

    # Relacionamento com outro Comentário (se o comentário é uma resposta)
    parent_comment = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    # Campos para tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Contadores
    likes_count = models.PositiveIntegerField(default=0)
    replies_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.user.username}: {self.content[:30]}..."

    class Meta:
        # Comentários mais recentes primeiro
        ordering = ['-created_at']

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Um usuário só pode curtir um comentário uma vez
        unique_together = ('user', 'comment')  
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} curtiu o comentário de ID: {self.comment.id}"
