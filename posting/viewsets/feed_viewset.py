from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posting.models import Post
from posting.serializers import PostSerializer

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Obtém o usuário autenticado
        user = request.user

        # Obtém os usuários que o usuário autenticado segue
        following = user.following.all()

        # Filtra as postagens feitas pelos usuários que ele segue
        posts = Post.objects.filter(user__in=following).order_by('-created_at')

        # Serializa as postagens
        serializer = PostSerializer(posts, many=True, context={'request': request})

        return Response(serializer.data)
