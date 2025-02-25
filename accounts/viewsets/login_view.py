from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User  # Aqui está o modelo customizado de usuário


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Verifique se o email e a senha foram fornecidos
        if not email or not password:
            return Response(
                {"detail": "Email e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Buscar o usuário pelo e-mail no modelo customizado
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {
                    "fields": ["email"],
                    "detail": "Nenhum usuário encontrado com esse email."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Verificar se a senha fornecida corresponde à do usuário
        if not user.check_password(password):
            return Response(
                {
                    "fields": ["email", "password"],
                    "detail": "Email ou senha inválido."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Gerar o JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response(
            {"refresh": str(refresh), "access": access_token}, status=status.HTTP_200_OK
        )
