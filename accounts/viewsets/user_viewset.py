from rest_framework import viewsets
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