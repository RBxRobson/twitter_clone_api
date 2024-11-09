from rest_framework import serializers
from accounts.models import User
from .profile_serializer import ProfileSerializer

class UserUpdateSerializer(serializers.ModelSerializer):
    # Permite o profile ser opcional para atualização
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'write_only': True, 'required': False}
        }

    def validate_username(self, value):
        # Verifica se o valor contém apenas caracteres permitidos
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError(
                "O username pode conter apenas letras, números e o caractere '_' e não pode conter espaços ou outros caracteres especiais."
            )
        return value

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        # Limpa campos vazios de validated_data para evitar sobrescrita no banco
        validated_data = {k: v for k, v in validated_data.items() if v not in [None, ""]}

        # Adiciona o '@' ao username se ele estiver presente em validated_data
        if 'username' in validated_data:
            validated_data['username'] = f"@{validated_data['username']}"

        # Atualiza a senha, se fornecida
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        # Atualiza os campos principais do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Atualiza o perfil, se dados do perfil forem fornecidos
        if profile_data:
            profile = instance.profile  
            for attr, value in profile_data.items():
                setattr(profile, attr, value)

            profile.save()

        return instance
