from django.db import models
from accounts.models import User

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

    @property
    def reposts_count(self):
        # Contabiliza reposts diretos e quotes
        return self.related_posts.filter(is_quote=False).count() + \
            self.related_posts.filter(is_quote=True).count()

    def __str__(self):
        return f"Post by {self.user.username}: {self.content[:30]}..."

    class Meta:
        # Exibe os posts mais recentes primeiro
        ordering = ['-created_at']  
