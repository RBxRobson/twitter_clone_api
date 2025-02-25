from rest_framework import serializers
from posting.models import Like, Post


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at", "user_details"]
        read_only_fields = ["id", "user", "created_at", "user_details"]

    def get_user_details(self, obj):
        profile = obj.user.profile
        return {
            "id": obj.user.id,
            "name": obj.user.name,
            "username": obj.user.username,
            "avatar": profile.avatar.url,
        }

    def validate(self, data):
        if not data.get("post"):
            raise serializers.ValidationError("Um like deve estar associado a um post.")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get("request")
        if request:
            if request.method == "GET":
                representation.pop("user", None)
            elif request.method == "POST":
                representation.pop("user_details", None)

        return representation
