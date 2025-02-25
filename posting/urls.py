from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter
from posting.viewsets import PostViewSet, FeedViewSet

# Roteador principal
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"feed", FeedViewSet, basename="feed")

# URLs finais
urlpatterns = [
    path("", include(router.urls)),
]
