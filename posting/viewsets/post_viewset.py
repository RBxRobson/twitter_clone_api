from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posting.models import Post
from posting.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    # Filtragem, ordenação e paginação podem ser aplicadas conforme a necessidade.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
