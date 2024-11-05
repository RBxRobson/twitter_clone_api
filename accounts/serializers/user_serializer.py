from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from accounts.models import User, Profile
from .profile_serializer import ProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])',
                message='A senha deve conter pelo menos uma letra minúscula, uma letra maiúscula e um número.',
            ),
        ],
        style={'input_type': 'password'}
    )
    profile = ProfileSerializer(required=False)  # Adiciona o serializer de perfil

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}  # Garantir que a senha não seja retornada
        }

    def validate_username(self, value):
        # Proíbe o uso de caracteres especiais e espaços
        if not value.isalnum() and '_' not in value:
            raise serializers.ValidationError("O username pode conter apenas letras, números e o caractere '_'.")
        if ' ' in value:
            raise serializers.ValidationError("O username não pode conter espaços.")

        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)  # Obtém os dados do perfil
        name = validated_data.get('name')

        # Gera o username automaticamente a partir do nome
        username = validated_data.get('username') or name.lower().replace(' ', '_')
        validated_data['username'] = f'@{username}'  # Adiciona o @

        # Criptografa a senha antes de salvar o usuário
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Cria o perfil se os dados forem fornecidos
        if profile_data:
            Profile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)  # Obtém os dados do perfil
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Criptografa a nova senha, se fornecida
        if password:
            instance.set_password(password)

        instance.save()

        # Atualiza o perfil se os dados forem fornecidos
        if profile_data:
            # Verifica se o perfil já existe e atualiza ou cria um novo
            Profile.objects.update_or_create(user=instance, defaults=profile_data)

        return instance

    def to_representation(self, instance):
        """Modifica a saída do JSON para incluir o campo profile."""
        representation = super().to_representation(instance)
        
        # Verifica se o profile existe antes de acessar seus atributos
        if hasattr(instance, 'profile'):
            representation['profile'] = {
                'bio': instance.profile.bio,
                'avatar': instance.profile.avatar.url if instance.profile.avatar else None,
                'header': instance.profile.header.url if instance.profile.header else None
            }
        else:
            representation['profile'] = None  # Caso o usuário não tenha um perfil

        return representation
