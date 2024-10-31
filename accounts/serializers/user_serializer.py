from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    # Campo de senha com validações específicas
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            # Valida que a senha tenha no mínimo 8 caracteres
            MinLengthValidator(8),
            # Valida que a senha contenha letras maiúsculas, minúsculas e números
            RegexValidator(
                regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])',
                message='A senha deve conter pelo menos uma letra minúscula, uma letra maiúscula e um número.',
            ),
        ],
        # Exibe a senha como campo oculto
        style={'input_type': 'password'}  
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'password']

    def create(self, validated_data):
        # Extrai e criptografa a senha antes de salvar o usuário
        password = validated_data.pop('password')
        user = User(**validated_data)
        # Usa o método de criptografia set_password
        user.set_password(password)  
        user.save()
        return user

    def update(self, instance, validated_data):
        # Atualiza o usuário e criptografa a senha, se fornecida
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Criptografa a nova senha, se fornecida
        if password:
            instance.set_password(password)
        instance.save()
        return instance
