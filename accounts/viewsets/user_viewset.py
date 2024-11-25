from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import User
from accounts.serializers import UserCreateSerializer, UserUpdateSerializer, UserDetailSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action in ['retrieve', 'list']:
            return UserDetailSerializer
        return UserCreateSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response({"detail": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user)
        return Response({"detail": f"Você agora está seguindo {user.username}."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response({"detail": "Você não pode deixar de seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user)
        return Response({"detail": f"Você deixou de seguir {user.username}."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.followers.all()
        data = [
            {
                'id': follower.id,
                'username': follower.username,
                'name': follower.name,
                'avatar': follower.profile.avatar.url,
                'bio': follower.profile.bio
            }
            for follower in followers
        ]
        return Response(data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()
        data = [
            {
                'id': following_user.id,
                'username': following_user.username,
                'name': following_user.name,
                'avatar': following_user.profile.avatar.url,
                'bio': following_user.profile.bio
            }
            for following_user in following
        ]
        return Response(data)