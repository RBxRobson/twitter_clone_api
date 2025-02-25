from django.db import models
from accounts.models import User


class Post(models.Model):
    ORIGINAL = "original"
    REPOST = "repost"
    QUOTE = "quote"
    COMMENT = "comment"

    POST_TYPES = [
        (ORIGINAL, "Original"),
        (REPOST, "Repost"),
        (QUOTE, "Quote"),
        (COMMENT, "Comment"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    post_type = models.CharField(max_length=10, choices=POST_TYPES, default=ORIGINAL)

    # Relacionamento para reposts, quotes e comentários
    original_post = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    # Conteúdo do post
    content = models.TextField(max_length=280, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.post_type == self.ORIGINAL:
            return f"Post de {self.user.username}: {self.content[:30]}..."
        elif self.post_type == self.QUOTE:
            return f"Citação de {self.user.username} sobre {self.original_post.id}: {self.content[:30]}..."
        elif self.post_type == self.REPOST:
            return f"Repost de {self.user.username} sobre {self.original_post.id}"
        elif self.post_type == self.COMMENT:
            return f"Comentário de {self.user.username} em {self.original_post.id}: {self.content[:30]}..."
