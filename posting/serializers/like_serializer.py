from rest_framework import serializers
from posting.models import Like, Post, Comment


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=False
    )
    comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False
    )

    class Meta:
        model = Like
        fields = ["id", "user", "post", "comment", "created_at", "user_details"]
        read_only_fields = ["id", "user", "created_at", "user_details"]

    def get_user_details(self, obj):
        # Obtém o perfil do usuário associado e retorna os dados completos
        profile = obj.user.profile
        return {
            "id": obj.user.id,
            "name": obj.user.name,
            "username": obj.user.username,
            "avatar": profile.avatar.url,
        }

    def validate(self, data):
        # Garante que o like está associado a um post OU a um comentário, mas não a ambos
        if not data.get("post") and not data.get("comment"):
            raise serializers.ValidationError(
                "Um like deve estar associado a um post ou a um comentário."
            )
        if data.get("post") and data.get("comment"):
            raise serializers.ValidationError(
                "Um like não pode estar associado a um post e a um comentário simultaneamente."
            )
        return data

    # Customiza a resposta com base no tipo de curtida.
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Método GET resposta
        request = self.context.get("request")
        if request and request.method == "GET":
            representation.pop("user", None)

        # Método Post resposta
        request = self.context.get("request")
        if request and request.method == "POST":
            representation.pop("user_details", None)

        # Remove o campo post caso seja uma curtida em comentário
        if instance.comment:
            representation.pop("post", None)
        # Remove o campo comment caso seja uma curtida em post
        else:
            representation.pop("comment", None)

        return representation
