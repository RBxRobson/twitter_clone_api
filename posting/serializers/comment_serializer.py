from rest_framework import serializers
from posting.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    # Contadores
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'content', 'post', 'parent_comment', 'user_details',
            'created_at', 'updated_at', 'likes_count', 'replies_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'likes_count', 'replies_count', 'user_details', 'user', 'post']

    # Retorna o número de likes associados ao comentário.
    def get_likes_count(self, obj):
        return obj.likes.count()

    # Retorna o número de respostas associadas ao comentário.
    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def get_user_details(self, obj):
        # Obtém o perfil do usuário associado e retorna os dados completos
        profile = obj.user.profile
        return {
            "id": obj.user.id,
            "name": obj.user.name,
            "username": obj.user.username,
            "avatar": profile.avatar.url
        }

    # Lista as respostas do comentário
    def get_replies(self, obj):
        if obj.parent_comment.exists():
            return CommentSerializer(obj.parent_comment.all(), many=True).data
        return []

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

        return representation
