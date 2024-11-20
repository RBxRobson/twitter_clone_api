from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from posting.models import Comment, Like, CommentLike, Post

@receiver(post_save, sender=Like)
def increase_likes_count(sender, instance, created, **kwargs):
    if created:
        instance.post.likes_count += 1
        instance.post.save()

@receiver(post_delete, sender=Like)
def decrease_likes_count(sender, instance, **kwargs):
    instance.post.likes_count -= 1
    instance.post.save()

# Incrementar o contador de comentários ao criar um comentário
@receiver(post_save, sender=Comment)
def increase_comments_count(sender, instance, created, **kwargs):
    if created and instance.post:
        instance.post.comments_count += 1
        instance.post.save()

# Decrementar o contador de comentários ao excluir um comentário
@receiver(post_delete, sender=Comment)
def decrease_comments_count(sender, instance, **kwargs):
    if instance.post:
        instance.post.comments_count -= 1
        instance.post.save()

@receiver(post_save, sender=CommentLike)
def increase_comment_likes_count(sender, instance, created, **kwargs):
    if created:
        instance.comment.likes_count += 1
        instance.comment.save()

@receiver(post_delete, sender=CommentLike)
def decrease_comment_likes_count(sender, instance, **kwargs):
    instance.comment.likes_count -= 1
    instance.comment.save()

@receiver(post_save, sender=Comment)
def increase_replies_count(sender, instance, created, **kwargs):
    if created and instance.parent_comment:
        instance.parent_comment.replies_count += 1
        instance.parent_comment.save()

@receiver(post_delete, sender=Comment)
def decrease_replies_count(sender, instance, **kwargs):
    if instance.parent_comment:
        instance.parent_comment.replies_count -= 1
        instance.parent_comment.save()

# Incrementar contadores ao criar reposts ou quotes
@receiver(post_save, sender=Post)
def update_reposts_count_on_create(sender, instance, created, **kwargs):
    if created and instance.original_post:
        if instance.is_quote:
            instance.original_post.quotes_count += 1
        instance.original_post.reposts_count += 1
        instance.original_post.save()

# Decrementar contadores ao excluir reposts ou quotes
@receiver(post_delete, sender=Post)
def update_reposts_count_on_delete(sender, instance, **kwargs):
    if instance.original_post:
        if instance.is_quote:
            instance.original_post.quotes_count -= 1
        instance.original_post.reposts_count -= 1
        instance.original_post.save()
