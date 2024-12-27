from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from accounts.models import User, Profile
from accounts.utils import get_unique_username


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])",
                message="A senha deve conter pelo menos uma letra minúscula, uma letra maiúscula e um número.",
            ),
        ],
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}  # Garantir que a senha não seja retornada
        }

    def create(self, validated_data):
        # Gera um nome de usuário único
        validated_data["username"] = get_unique_username(validated_data.get("name"))

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Criação direta do perfil com valores padrões
        Profile.objects.create(user=user)

        return user
