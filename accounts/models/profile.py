from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User

# Função para definir o caminho de upload dinâmico
def user_directory_path(instance, filename):
    # O arquivo será salvo em `media/user_<username>/<filename>`
    return f'user_{instance.user.username}/{filename}'

class Profile(models.Model):
    # O campo user atua como a chave primária do Profile, compartilhando o mesmo ID
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    
    # As imagens serão salvas em um diretório específico para cada usuário
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, default='media/placeholders/avatar_placeholder.png')
    header = models.ImageField(upload_to=user_directory_path, blank=True, default='media/placeholders/header_placeholder.png')
    
    # Campos que podem ser modificados pelo usuário
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        # Atualiza os campos name e username do User sempre que o Profile for salvo
        if self.user.name != self.name or self.user.username != self.username:
            self.user.name = self.name
            self.user.username = self.username
            self.user.save()
        super(Profile, self).save(*args, **kwargs)

# Sinal para criar automaticamente um Profile quando um User é criado
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
