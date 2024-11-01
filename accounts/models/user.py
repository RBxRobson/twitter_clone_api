from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Gerenciador personalizado de usuários
class UserManager(BaseUserManager):
    # Método para criar um usuário comum
    def create_user(self, username, email, password=None, **extra_fields):
        # Verifica se o email foi fornecido
        if not email:
            raise ValueError('O email deve ser fornecido')
        # Verifica se o username foi fornecido
        if not username:
            raise ValueError('O username deve ser fornecido')

        # Normaliza o email e cria o usuário
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        # Criptografa a senha
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Método para criar um superusuário
    def create_superuser(self, username, email, password=None, **extra_fields):
        # Define permissões de administrador para o superusuário
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# Modelo de usuário customizado
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    # Status do usuário
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Campo usado como identificador único para autenticação
    USERNAME_FIELD = 'username'
    # Campos obrigatórios adicionais para criação de superusuários
    REQUIRED_FIELDS = ['email']

    # Associa o gerenciador personalizado ao modelo
    objects = UserManager()

    # Representação do usuário
    def __str__(self):
        return self.username


