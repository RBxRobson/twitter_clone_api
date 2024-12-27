from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Gerenciador personalizado de usuários
class UserManager(BaseUserManager):
    # Método para criar um usuário comum
    def create_user(self, name, email, password=None, **extra_fields):
        # Verifica se o email foi fornecido
        if not email:
            raise ValueError("O email deve ser fornecido")

        # Normaliza o email e cria o usuário
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)

        # Criptografa a senha
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Método para criar um superusuário
    def create_superuser(self, name, email, password=None, **extra_fields):
        # Define permissões de administrador para o superusuário
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(name, email, password, **extra_fields)


# Modelo de usuário customizado
class User(AbstractBaseUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    # Relacionamentos para seguidores e seguidos
    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False, blank=True
    )

    # Campos de tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Status do usuário
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Campo usado como identificador único para autenticação
    USERNAME_FIELD = "username"
    # Campos obrigatórios adicionais para criação de superusuários
    REQUIRED_FIELDS = ["email", "name"]

    # Associa o gerenciador personalizado ao modelo
    objects = UserManager()

    # Representação do usuário
    def __str__(self):
        return self.username
