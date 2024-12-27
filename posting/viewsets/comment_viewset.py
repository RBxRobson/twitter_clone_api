from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from django.core.exceptions import ValidationError
from posting.models import Comment, Post, Like
from posting.serializers import CommentSerializer, LikeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Restringe os comentários ao post relacionado, sem incluir respostas
    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs["post_pk"], parent_comment=None
        )

    # Define automaticamente o user com base no usuário autenticado e o post de acordo com o id na rota
    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs["post_pk"])
        parent_comment = None
        # Tenta obter o 'comment_pk' da URL, mas se não existir, será None
        if "comment_pk" in self.kwargs:
            parent_comment = Comment.objects.get(
                post_id=post, id=self.kwargs["comment_pk"]
            )

        # Validação de post
        if not post:
            raise ValidationError("Um comentário deve ter ligação com uma postagem.")

        # Bloquear comentários em um repost
        if post.post_type == Post.REPOST:
            raise ValidationError("Não é possível comentar em um repost.")

        # Validações para comentários de resposta
        if parent_comment:
            # Garante que, se houver um comentário resposta, ele possua um post relacionado
            if not post:
                raise ValidationError(
                    "Um comentário de resposta deve ter ligação com algum post"
                )
            # Garante que, se houver um comentário pai, ele pertença ao mesmo post
            if parent_comment.post != post:
                raise ValidationError(
                    "O comentário pai deve pertencer ao mesmo post que este comentário."
                )

        serializer.save(user=self.request.user, post=post)

    # Adiciona ou lista as respostas de um comentário.
    @action(detail=True, methods=["GET", "POST"], url_path="replies")
    def replies(self, request, post_pk=None, pk=None):
        try:
            post = Post.objects.get(id=post_pk)
            comment = Comment.objects.get(id=pk, post=post)
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return Response(
                {"detail": "Comentário ou post não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "POST":
            # Adiciona uma nova resposta ao comentário
            data = {**request.data, "parent_comment": pk, "post": post_pk}
            serializer = CommentSerializer(data=data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Lista as respostas do comentário
        replies = comment.replies.all()
        serializer = CommentSerializer(replies, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["GET", "POST", "DELETE"], url_path="likes")
    def likes(self, request, post_pk=None, pk=None):

        try:
            post = Post.objects.get(id=post_pk)
            comment = Comment.objects.get(id=pk, post=post)
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return Response(
                {"detail": "Comentário ou post não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        user = request.user

        if request.method == "GET":
            # Lista todos os likes do comentário
            likes = Like.objects.filter(comment=comment)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            # Adiciona um like ao comentário
            if Like.objects.filter(comment=comment, user=user).exists():
                return Response(
                    {"detail": "Você já curtiu este comment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            like = Like.objects.create(comment=comment, user=user)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            # Remove o like do comentário para o usuário atual
            try:
                like = Like.objects.get(comment=comment, user=user)
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Like.DoesNotExist:
                return Response(
                    {"detail": "Você não curtiu este post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
