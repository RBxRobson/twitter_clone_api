from rest_framework import serializers
from posting.models import Comment, CommentLike, Post
from accounts.models import User

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'post', 'parent_comment', 'created_at', 'updated_at', 'likes_count', 'replies_count']
        read_only_fields = ['created_at', 'updated_at', 'likes_count', 'replies_count']

    def validate(self, data):
        # Verifica se o comentário está sendo feito no post ou em outro comentário
        if not data.get('post') and not data.get('parent_comment'):
            raise serializers.ValidationError("A comment must be related to a post or another comment.")
        return data
    
    def create(self, validated_data):
        # Criação do comentário
        comment = Comment.objects.create(**validated_data)
        return comment

    def get_replies(self, obj):
        # Lista as respostas do comentário
        if obj.parent_comment.exists():
            return CommentSerializer(obj.parent_comment.all(), many=True).data
        return []

class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        # Verifica se o usuário já curtiu o comentário
        if CommentLike.objects.filter(user=data['user'], comment=data['comment']).exists():
            raise serializers.ValidationError("You have already liked this comment.")
        return data

    def create(self, validated_data):
        # Cria o like no comentário
        comment_like = CommentLike.objects.create(**validated_data)
        return comment_like
