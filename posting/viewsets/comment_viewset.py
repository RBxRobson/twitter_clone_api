from rest_framework import viewsets
from posting.models import Comment, CommentLike
from posting.serializers import CommentSerializer, CommentLikeSerializer
from rest_framework.permissions import IsAuthenticated

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Obtém o ID do post da rota
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Obtém o ID do comentário da rota
        comment_id = self.kwargs.get('comment_pk')
        return CommentLike.objects.filter(comment_id=comment_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra respostas com base no comentário pai
        comment_id = self.kwargs.get('comment_pk')
        return Comment.objects.filter(parent_comment=comment_id)

    def perform_create(self, serializer):
        # Associa automaticamente o comentário pai e o usuário
        parent_comment = Comment.objects.get(pk=self.kwargs.get('comment_pk'))
        serializer.save(user=self.request.user, parent=parent_comment)