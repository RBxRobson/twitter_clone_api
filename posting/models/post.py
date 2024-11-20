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
            return f"{'Quote' if self.is_quote else 'Repost'} by {self.user.username}: {self.content[:30]}..."
        return f"Post by {self.user.username}: {self.content[:30]}..."

    def clean(self):
        """
        Validações:
        - Um post marcado como is_quote=True deve ter um original_post.
        - Um repost ou quote não pode referenciar outro repost ou quote.
        """
        if self.is_quote and not self.original_post:
            raise ValidationError("A quote must reference an original post.")
        if self.original_post and self.original_post.original_post:
            raise ValidationError("A repost cannot reference another repost.")
        super().clean()

    class Meta:
        # Exibe os posts mais recentes primeiro
        ordering = ['-created_at']
        indexes = [
            # Otimização de consultas
            models.Index(fields=['original_post', 'is_quote']),  
        ]
