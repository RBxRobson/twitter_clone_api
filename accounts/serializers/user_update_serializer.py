import unicodedata
from rest_framework import serializers
from accounts.models import User
from .profile_serializer import ProfileSerializer
from django.core.validators import MinLengthValidator, RegexValidator


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    old_password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
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
        fields = [
            "id",
            "name",
            "username",
            "email",
            "password",
            "profile",
            "old_password",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"required": False},
            "username": {"required": False},
            "email": {"required": False},
            "password": {"write_only": True, "required": False},
            "profile": {"required": False},
        }

    def validate(self, attrs):
        # Verifica se o JSON está vazio
        if not attrs:
            raise serializers.ValidationError(
                "Nenhum dado foi fornecido para atualização."
            )

        # Verifica se a alteração de senha exige a senha antiga
        if "password" in attrs and "old_password" not in attrs:
            raise serializers.ValidationError(
                {"old_password": "A senha antiga é obrigatória para alterar a senha."}
            )

        # Verifica se a senha antiga está correta
        if "old_password" in attrs:
            user = self.instance  # Instância do usuário sendo atualizada
            if not user.check_password(attrs["old_password"]):
                raise serializers.ValidationError(
                    {"old_password": "A senha antiga está incorreta."}
                )

        # Verifica se a nova senha é igual à antiga
        if "password" in attrs and "old_password" in attrs:
            user = self.instance
            if user.check_password(attrs["password"]):
                raise serializers.ValidationError(
                    {"password": "A nova senha não pode ser igual à senha antiga."}
                )

        return attrs

    def validate_username(self, value):
        # Remove acentos do valor
        value_no_accents = ''.join(
            c for c in unicodedata.normalize('NFD', value) if unicodedata.category(c) != 'Mn'
        )
        
        # Verifica se o valor contém apenas caracteres permitidos
        if not value_no_accents.replace("_", "").isalnum():
            raise serializers.ValidationError(
                "O username pode conter apenas letras, números e o caractere '_' e não pode conter espaços ou outros caracteres especiais, incluindo acentuação."
            )
        
        # Verifica se o username já existe
        if User.objects.filter(username=value_no_accents).exists():
            raise serializers.ValidationError(
            "Este nome de usuário já está em uso. Por favor, escolha outro."
        )
        
        return value_no_accents

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)

        # Remove a senha antiga dos dados validados
        validated_data.pop("old_password", None)

        # Limpa campos vazios, exceto o campo `bio` dentro de `profile`
        validated_data = {
            k: v for k, v in validated_data.items() if v not in [None, ""]
        }
        
        # Adiciona o '@' ao username se ele estiver presente em validated_data
        if "username" in validated_data:
            validated_data["username"] = f"@{validated_data['username']}"

        # Atualiza a senha, se fornecida
        if "password" in validated_data:
            instance.set_password(validated_data.pop("password"))

        # Atualiza os campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Atualiza o perfil, mantendo `bio` como um campo que pode ser vazio
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                if value not in [None, ""] or attr == "bio":  # Permite apenas bio ser vazio
                    setattr(profile, attr, value)

            profile.save()

        return instance
