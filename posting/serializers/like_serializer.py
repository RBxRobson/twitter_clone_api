from rest_framework import serializers
from posting.models import Like, Post
from accounts.models import User

class LikeSerializer(serializers.ModelSerializer):
    # Relacionamento com o usuário
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    
    # Relacionamento com o post
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        # Verifica se o usuário já curtiu o post
        if Like.objects.filter(user=data['user'], post=data['post']).exists():
            raise serializers.ValidationError("Você já curtiu o post.")
        return data

    def create(self, validated_data):
        # Cria a curtir (like) se a validação passar
        like = Like.objects.create(**validated_data)
        return like
