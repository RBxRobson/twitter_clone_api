from django.db import models
from accounts.models import User
from posting.models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=280)

    # Auto-referência para suporte a comentários aninhados
    parent_comment = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )

    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.parent_comment:
            return f'Reply by {self.author.username} on comment {self.parent_comment.id}'
        return f'Comment by {self.author.username} on post {self.post.id} at {self.created_at}'