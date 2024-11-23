from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from posting.viewsets import PostViewSet, LikeViewSet, CommentViewSet, CommentLikeViewSet, ReplyViewSet
# Roteador principal
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# Roteadores aninhados para interações em um post
posts_router = NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'likes', LikeViewSet, basename='post-likes')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

# Roteador aninhado para interações em comentários
comments_router = NestedDefaultRouter(posts_router, r'comments', lookup='comment')
comments_router.register(r'likes', CommentLikeViewSet, basename='comment-likes')
comments_router.register(r'replies', ReplyViewSet, basename='comment-replies')

urlpatterns = router.urls + posts_router.urls + comments_router.urls
