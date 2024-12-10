from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from posting.viewsets import PostViewSet, CommentViewSet, FeedViewSet

# Roteador principal
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'feed', FeedViewSet, basename='feed')

# Nested routers para comentários relacionados a posts
post_comments_router = NestedSimpleRouter(router, r'posts', lookup='post')
post_comments_router.register(r'comments', CommentViewSet, basename='post-comments')

# URLs finais
urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_comments_router.urls)),
]
