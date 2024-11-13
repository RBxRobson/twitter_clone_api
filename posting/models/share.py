from django.db import models
from accounts.models import User
from posting.models import Post

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    created_at = models.DateTimeField(auto_now_add=True)
    is_direct = models.BooleanField(default=True)
    perspective = models.TextField(blank=True, null=True, max_length=400) 
    
    # Contadores de interações no compartilhamento - apenas se não for direto
    like_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    comment_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    share_count = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        if self.is_direct:
            return f'{self.user.username} directly shared post {self.post.id}'
        else:
            return f'{self.user.username} shared post {self.post.id} with perspective'

    class Meta:
        unique_together = ('user', 'post', 'is_direct')

    def save(self, *args, **kwargs):
        # Se o compartilhamento for direto, não mantém os contadores de interação
        if self.is_direct:
            self.like_count = 0
            self.comment_count = 0
            self.share_count = 0
        super().save(*args, **kwargs)

