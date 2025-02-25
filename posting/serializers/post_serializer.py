from rest_framework import serializers
from posting.models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()
    original_post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=False, allow_null=True
    )
    
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    quotes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_reposted = serializers.SerializerMethodField()
    is_following_author = serializers.SerializerMethodField() 

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "user_details",
            "content",
            "post_type",
            "original_post",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "reposts_count",
            "quotes_count",
            "is_liked",
            "is_reposted",
            "is_following_author",
        ]
        read_only_fields = [
            "created_at",
            "user",
            "user_details",
            "updated_at",
            "likes_count",
            "comments_count",
            "reposts_count",
            "quotes_count",
            "is_liked",
            "is_reposted",
            "is_following_author"
        ]

    def get_original_post(self, obj):
        """Retorna os detalhes completos do post original em vez do ID."""
        if obj.original_post:
            return PostSerializer(obj.original_post, context=self.context).data
        return None

    def get_user_details(self, obj):
        profile = obj.user.profile
        return {
            "id": obj.user.id,
            "name": obj.user.name,
            "username": obj.user.username,
            "avatar": profile.avatar.url,
        }

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return Post.objects.filter(original_post=obj, post_type=Post.COMMENT).count()


    def get_reposts_count(self, obj):
        return obj.interactions.filter(post_type=Post.REPOST).count()

    def get_quotes_count(self, obj):
        return obj.interactions.filter(post_type=Post.QUOTE).count()

    def get_is_liked(self, obj):
        # Checa se o usuário atual (obtido do request) curtiu o post
        user = self.context.get("request").user
        return obj.likes.filter(user=user).exists()

    def get_is_reposted(self, obj):
        # Checa se o usuário atual fez um repost
        user = self.context.get("request").user
        repost = obj.interactions.filter(user=user, post_type=Post.REPOST).first()
    
        return repost.id if repost else False
    
    def get_is_following_author(self, obj):
        # Verifica se o usuário autenticado segue o autor da postagem.
        request = self.context.get("request")
        if request.user.id == obj.user.id:
            return None

        return obj.user.followers.filter(id=request.user.id).exists()

    def validate(self, data):
        # Obtém o objeto atual (para requisições PUT)
        instance = self.instance

        # Obtém o valor atual de `post_type` do objeto caso não esteja nos dados
        post_type = data.get("post_type", instance.post_type if instance else None)
        content = data.get("content", "").strip()
        original_post = data.get("original_post")

        if not post_type:
            raise serializers.ValidationError(
                "O campo post_type é obrigatório (original, repost, quote ou comment)."
            )

        # Validações para postagens originais
        if post_type == Post.ORIGINAL:
            if original_post:
                raise serializers.ValidationError(
                    "Uma postagem original não pode referenciar outra postagem."
                )
            if not content:
                raise serializers.ValidationError(
                    "Uma postagem original deve possuir conteúdo."
                )

        # Validações para citações
        if post_type == Post.QUOTE:
            if not original_post:
                raise serializers.ValidationError(
                    "Uma citação deve referenciar um post original."
                )
            if not content:
                raise serializers.ValidationError(
                    "Uma citação deve possuir conteúdo autoral."
                )

        # Validações para reposts
        if post_type == Post.REPOST:
            if original_post and original_post.post_type == Post.REPOST:
                raise serializers.ValidationError(
                    "Um repost deve referenciar uma postagem original, ou uma citação."
                )   
            if not original_post:
                raise serializers.ValidationError(
                    "Um repost deve referenciar um post original."
                )
            if content:
                raise serializers.ValidationError(
                    "Um repost não pode ter conteúdo autoral."
                )

        # Validações para comentários
        if post_type == Post.COMMENT:
            if original_post and original_post.post_type == Post.REPOST:
                raise serializers.ValidationError(
                    "Um comentário deve referenciar uma postagem original, uma citação ou outro comentário"
                )   
            if not original_post:
                raise serializers.ValidationError(
                    "Um comentário deve referenciar algum comentário ou postagem."
                )
            if not content:
                raise serializers.ValidationError(
                    "Um comentário deve ter conteúdo."
                )
    
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")

        # Se for um GET, trocar o ID pelo objeto serializado
        if instance.original_post:
            representation["original_post"] = self.get_original_post(instance)

        # Método GET resposta
        if request and request.method == "GET":
            representation.pop("user", None)

        # Método POST resposta
        if request and request.method == "POST":
            representation.pop("user_details", None)

        # Remove contadores irrelevantes para REPOST
        if instance.post_type == Post.REPOST:
            representation.pop("reposts_count", None)
            representation.pop("quotes_count", None)
            representation.pop("likes_count", None)
            representation.pop("comments_count", None)
            representation.pop("is_liked", None)
            representation.pop("is_reposted", None)

        return representation
