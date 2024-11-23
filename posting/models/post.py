from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

class Post(models.Model):
    # Relaciona o post a um usuário
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    # Conteúdo do post (limite baseado no padrão do Twitter)
    content = models.TextField(max_length=280, blank=True, default='')

    # Post original para citações (quotes) e repostagens
    original_post = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='related_posts'
    )

    # Indica se o post é uma citação (quote)
    is_quote = models.BooleanField(default=False)

    # Campos para tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Contadores
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    reposts_count = models.PositiveIntegerField(default=0)
    quotes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.original_post:
            return f"{'Citação' if self.is_quote else 'Repostagem'} de {self.user.username}: {self.content[:30]}..."
        return f"Postagem de {self.user.username}: {self.content[:30]}..."

    class Meta:
        # Exibe os posts mais recentes primeiro
        ordering = ['-created_at']
        indexes = [
            # Otimização de consultas
            models.Index(fields=['original_post', 'is_quote']),  
        ]
