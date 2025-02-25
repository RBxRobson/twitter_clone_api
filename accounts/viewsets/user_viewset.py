import random
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from accounts.models import User
from posting.models import Post
from posting.serializers import PostSerializer
from accounts.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserDetailSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action in ["retrieve", "list"]:
            return UserDetailSerializer
        return UserCreateSerializer
    
    def get_object(self):
        lookup_field = self.kwargs.get("pk")
        try:
            # Verifica se o parâmetro é um número (ID)
            user = User.objects.get(pk=int(lookup_field))
        except (User.DoesNotExist, ValueError):
            # Caso contrário, assume que é um username e remove o `@` para a busca
            try:
                user = User.objects.get(username=f"@{lookup_field.lstrip('@')}")
            except User.DoesNotExist:
                raise NotFound(detail="Usuário não encontrado.")
        return user
    
    def get_parser_classes(self):
        """Define os parsers dinamicamente com base no método HTTP."""
        if self.request.method == "PUT":
            return [MultiPartParser(), FormParser()]
        return [JSONParser()]

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def posts(self, request, pk=None):
        user = self.get_object()

        # Recupera os posts do usuário, excluindo os do tipo COMMENT
        posts = Post.objects.filter(user=user).exclude(post_type='comment')

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "Você não pode seguir a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.add(user)
        return Response(
            {"detail": f"Você agora está seguindo {user.username}."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "Você não pode deixar de seguir a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.remove(user)
        return Response(
            {"detail": f"Você deixou de seguir {user.username}."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.followers.all()
        serializer = UserDetailSerializer(followers, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()
        serializer = UserDetailSerializer(following, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = UserDetailSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def recommendations(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        recommendations = User.objects.exclude(Q(id=user.id) | Q(followers=user))

        head_user = recommendations.filter(id=1).first()
        other_users = list(recommendations.exclude(id=1))
        random.shuffle(other_users)

        ordered_recommendations = [head_user] + other_users if head_user else other_users

        serializer = UserDetailSerializer(ordered_recommendations, many=True, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

