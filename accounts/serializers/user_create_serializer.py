from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import MinLengthValidator, RegexValidator
from accounts.models import User, Profile
from accounts.utils import get_unique_username


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Já existe um usuário com este e-mail."
            ),
        ]
    )
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
            # Garante que a senha não seja retornada
            "password": {"write_only": True}
        }

    def validate(self, data):
        # Gera um nome de usuário único
        data["username"] = get_unique_username(data.get("name"))

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Criação direta do perfil com valores padrões
        Profile.objects.create(user=user)

        return user
