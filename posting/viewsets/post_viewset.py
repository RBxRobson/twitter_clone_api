from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from accounts.serializers import UserDetailSerializer
from posting.models import Post, Like
from posting.serializers import PostSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Post.objects.all()
        
        # Se for uma busca direta (listagem), excluir comentários
        if self.action == "list":
            queryset = queryset.exclude(post_type=Post.COMMENT)
        
        return queryset

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
        # Verifica se o usuário já curtiu o post
            like = Like.objects.filter(post=post, user=user).first()
        if like:
            # Se já curtiu, remove o like
            like.delete()
            return Response(
                {"detail": "Like removido com sucesso."},
                status=status.HTTP_200_OK,
            )
        else:
            # Caso contrário, adiciona o like
            like = Like.objects.create(post=post, user=user)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["GET"], url_path="quotes")
    def quotes(self, request, pk=None):
        # Lista os quotes de um post.
        post = self.get_object()
        quotes = Post.objects.filter(original_post=post, post_type=Post.QUOTE)
        serializer = self.get_serializer(quotes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="reposts")
    def reposts(self, request, pk=None):
        post = self.get_object()
        reposts = Post.objects.filter(original_post=post, post_type=Post.REPOST).select_related("user__profile")

        # Passando o contexto corretamente
        data = [UserDetailSerializer(repost.user, context={"request": request}).data for repost in reposts]

        return Response(data)
    
    @action(detail=True, methods=["GET"], url_path="comments")
    def comments(self, request, pk=None):
        # Lista os comentários de um post.
        post = self.get_object()
        comments = Post.objects.filter(original_post=post, post_type=Post.COMMENT)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)