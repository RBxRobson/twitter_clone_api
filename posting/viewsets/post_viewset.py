from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from posting.models import Post, Like
from posting.serializers import PostSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Define automaticamente o user com base no usuário autenticado
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["GET", "POST", "DELETE"], url_path="likes")
    def likes(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if request.method == "GET":
            # Lista todos os likes do post
            likes = Like.objects.filter(post=post)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            # Adiciona um like ao post
            if Like.objects.filter(post=post, user=user).exists():
                return Response(
                    {"detail": "Você já curtiu este post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            like = Like.objects.create(post=post, user=user)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            # Remove o like do post para o usuário atual
            try:
                like = Like.objects.get(post=post, user=user)
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Like.DoesNotExist:
                return Response(
                    {"detail": "Você não curtiu este post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(detail=True, methods=["GET"], url_path="quotes")
    def quotes(self, request, pk=None):
        # Lista os quotes de um post.
        post = self.get_object()
        quotes = Post.objects.filter(original_post=post, post_type=Post.QUOTE)
        serializer = self.get_serializer(quotes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="reposts")
    def reposts(self, request, pk=None):
        # Lista os reposts de um post.
        post = self.get_object()
        reposts = Post.objects.filter(original_post=post, post_type=Post.REPOST)
        serializer = self.get_serializer(reposts, many=True)
        return Response(serializer.data)
