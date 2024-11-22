from rest_framework import serializers
from posting.models import Post
from accounts.models import User

class PostSerializer(serializers.ModelSerializer):
    # Campo de usuário pode ser representado como um nome de usuário ou ID
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    # Representação de original_post
    original_post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    # Campos de contagem podem ser excluídos da entrada (somente leitura)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    reposts_count = serializers.IntegerField(read_only=True)
    quotes_count = serializers.IntegerField(read_only=True)

    def validate(self, data):
        original_post = data.get('original_post')
        is_quote = data.get('is_quote')
        content = data.get('content', '').strip()

        # Validação para postagens
        if not is_quote and not original_post:
            if not content:
                raise serializers.ValidationError("Uma postagem deve possuir conteúdo.")

        # Validações específicas para citações
        if is_quote:
            if not original_post:
                raise serializers.ValidationError("Uma citação deve referenciar um post original.")
            if not content:
                raise serializers.ValidationError("Uma citação deve possuir conteúdo autoral.")

        # Validações específicas para reposts
        if original_post:
            # Validação para reposts em cadeia
            if original_post.original_post:
                raise serializers.ValidationError("Um repost não pode referenciar outro repost ou citação.")
            if content and not is_quote:
                raise serializers.ValidationError("Um repost não pode ter conteúdo autoral.")

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Ajusta os contadores para reposts
        if instance.original_post and not instance.is_quote:
            # Para reposts, marca os contadores como None
            representation['likes_count'] = None
            representation['comments_count'] = None
            representation['reposts_count'] = None
            representation['quotes_count'] = None

        # Ajusta os contadores para citações
        if instance.is_quote:
            # Para citações, remove os contadores de reposts e quotes
            representation['reposts_count'] = None
            representation['quotes_count'] = None

        return representation


    class Meta:
        model = Post
        fields = [
            'id', 'user', 'content', 'original_post', 'is_quote', 
            'created_at', 'updated_at', 'likes_count', 'comments_count', 
            'reposts_count', 'quotes_count'
        ]
        read_only_fields = ['likes_count', 'comments_count', 'reposts_count', 'quotes_count']
