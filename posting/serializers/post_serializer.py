from rest_framework import serializers
from posting.models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()

    # Representação de original_post
    original_post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True)

    # Campos read-only para os contadores de interações
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    quotes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'user_details', 'content', 'post_type', 'original_post',
            'created_at', 'updated_at', 'likes_count', 'comments_count',
            'reposts_count', 'quotes_count',
        ]
        read_only_fields = [
            'created_at', 'user', 'user_details', 'updated_at',
            'likes_count', 'comments_count', 'reposts_count', 'quotes_count'
        ]

    def get_user_details(self, obj):
        # Obtém o perfil do usuário associado e retorna os dados completos
        profile = obj.user.profile
        return {
            "id": obj.user.id,
            "name": obj.user.name,
            "username": obj.user.username,
            "avatar": profile.avatar.url
        }

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_reposts_count(self, obj):
        return obj.interactions.filter(post_type=Post.REPOST).count()

    def get_quotes_count(self, obj):
        return obj.interactions.filter(post_type=Post.QUOTE).count()

    def validate(self, data):
        # Validação permanece a mesma
        post_type = data.get('post_type')
        content = data.get('content', '').strip()
        original_post = data.get('original_post')

        if not post_type:
            raise serializers.ValidationError("O campo post_type é obrigatório (original, repost ou quote).")

        # Validações para postagens originais
        if post_type == Post.ORIGINAL:
            if original_post:
                raise serializers.ValidationError("Uma postagem original não pode referenciar outra postagem.")
            if not content:
                raise serializers.ValidationError("Uma postagem original deve possuir conteúdo.")
        
        # Validações para citações
        if post_type == Post.QUOTE:
            if original_post and original_post.post_type != Post.ORIGINAL:
                raise serializers.ValidationError("A citação deve referenciar uma postagem original.")
            if not original_post:
                raise serializers.ValidationError("Uma citação deve referenciar um post original.")
            if not content:
                raise serializers.ValidationError("Uma citação deve possuir conteúdo autoral.")

        # Validações para reposts
        if post_type == Post.REPOST:
            if original_post and original_post.post_type != Post.ORIGINAL:
                raise serializers.ValidationError("Um repost deve referenciar uma postagem original.")
            if not original_post:
                raise serializers.ValidationError("Um repost deve referenciar um post original.")
            if content:
                raise serializers.ValidationError("Um repost não pode ter conteúdo autoral.")

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Método GET resposta
        request = self.context.get('request')
        if request and request.method == 'GET':
            representation.pop('user', None)

        # Método Post resposta
        request = self.context.get('request')
        if request and request.method == 'POST':
            representation.pop('user_details', None)

        # Remove contadores irrelevantes para QUOTE e REPOST
        if instance.post_type in [Post.QUOTE, Post.REPOST]:
            representation.pop('reposts_count', None)
            representation.pop('quotes_count', None)

        # Remove contadores irrelevantes para REPOST
        if instance.post_type == Post.REPOST:
            representation.pop('likes_count', None)
            representation.pop('comments_count', None)

        return representation
