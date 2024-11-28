from django.db import models
from accounts.models import User
from .post import Post

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    
    # O comentário pode ser em um post ou resposta a outro comentário
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="replies"
    )

    # Conteúdo do comentário
    content = models.TextField(max_length=280)

    # Campos de tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ordena os comentários mais recentes primeiro
        ordering = ['-created_at']

    def __str__(self):
        if self.parent_comment:
            return f"Resposta de {self.user.username} a {self.parent_comment.user.username}: {self.content[:30]}..."
        else:
            return f"Comentário de {self.user.username} no post {self.post.id}: {self.content[:30]}..."