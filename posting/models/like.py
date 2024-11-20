from django.db import models
from accounts.models import User
from posting.models import Post

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Evita duplicatas (um usuário só pode curtir um post uma vez)
        unique_together = ('user', 'post')  
        # Likes mais recentes primeiro
        ordering = ['-created_at']  

    def __str__(self):
        return f"{self.user.username} liked Post ID {self.post.id}"

