from rest_framework import viewsets
from posting.models import Like
from posting.serializers import LikeSerializer
from rest_framework.permissions import IsAuthenticated

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Obtém o ID do post da rota
        post_id = self.kwargs.get('post_pk')  
        return Like.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
