from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserDetailSerializer

class UserSearchViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request):
        search_term = request.query_params.get("q", "").strip()

        if not search_term:
            return Response(
                {"detail": "Nenhum termo de pesquisa fornecido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Busca flexível por nome e username
        users_by_name = User.objects.filter(name__icontains=search_term)
        users_by_username = User.objects.filter(username__icontains=search_term)

        users = users_by_name | users_by_username

        if not users.exists():
            return Response(
                {"detail": "Nenhum usuário encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserDetailSerializer(users, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
