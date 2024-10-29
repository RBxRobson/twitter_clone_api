from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Gerenciador de usuários personalizado
class UserManager(BaseUserManager):
    # Método para criar um usuário normal
    def create_user(self, username, email, password=None, **extra_fields):
        # Verifica se o email foi fornecido
        if not email:
            raise ValueError('O email deve ser fornecido')
        # Verifica se o username foi fornecido
        if not username:
            raise ValueError('O username deve ser fornecido')

        # Normaliza o email
        email = self.normalize_email(email)
        # Cria uma nova instância de usuário
        user = self.model(username=username, email=email, **extra_fields)
        # Define a senha do usuário
        user.set_password(password)
        # Salva o usuário no banco de dados
        user.save(using=self._db)
        return user

    # Método para criar um superusuário
    def create_superuser(self, username, email, password=None, **extra_fields):
        # Define o superusuário como ativo e com acesso ao admin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

# Modelo de usuário
class User(AbstractBaseUser):
    # Chave primária auto incrementável
    id = models.AutoField(primary_key=True)
    # Nome do usuário
    name = models.CharField(max_length=50)
    # Nome de usuário único
    username = models.CharField(max_length=50, unique=True)
    # Email único com validação
    email = models.EmailField(
        max_length=100,
        unique=True,
        validators=[
            EmailValidator()])
    # Senha com validação
    password = models.CharField(
        max_length=100,
        validators=[
            # Valida o comprimento mínimo da senha
            MinLengthValidator(8),
            # Valida a complexidade da senha (mínimo uma letra maiúscula,
            # minúscula e número)
            RegexValidator(
                regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])',
                message='A senha deve conter pelo menos uma letra minúscula, uma letra maiúscula e um número.',
            ),
        ],
    )

    # Campo que indica se o usuário está ativo
    is_active = models.BooleanField(default=True)
    # Campo que indica se o usuário tem acesso ao admin
    is_staff = models.BooleanField(default=False)

    # Campo que será usado para autenticação
    USERNAME_FIELD = 'username'
    # Campos obrigatórios para a criação do usuário
    REQUIRED_FIELDS = ['email']

    # Gerenciador de usuários
    objects = UserManager()

    # Representação do objeto
    def __str__(self):
        return self.username
