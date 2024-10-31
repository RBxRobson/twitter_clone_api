from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import User
from accounts.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    # Define o conjunto de dados e o serializer usado pela viewset
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Permite criação de usuários sem autenticação
        if self.action == 'create':
            return [AllowAny()]
        # Exige autenticação para outras ações
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # Salva o usuário usando o serializer
        serializer.save()
