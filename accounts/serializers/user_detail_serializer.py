from rest_framework import serializers
from accounts.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "profile",
            "followers_count",
            "following_count",
            "is_following",
            "created_at",
            "updated_at",
        ]

    def get_profile(self, instance):
        return {
            "bio": instance.profile.bio,
            "avatar": instance.profile.avatar.url,
            "header": instance.profile.header.url,
            "updated_at": instance.profile.updated_at,
        }

    def get_followers_count(self, instance):
        return instance.followers.count()

    def get_following_count(self, instance):
        return instance.following.count()
    
    def get_is_following(self, instance):
        """Verifica se o usuário autenticado está seguindo o usuário serializado."""
        request = self.context.get("request")
        if request and request.user.id == instance.id:
            return None  # Ou False, se preferir
        return instance.followers.filter(id=request.user.id).exists()
    
    def to_representation(self, instance):
        """Remove o campo is_following quando o usuário autenticado for o próprio usuário serializado."""
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.id == instance.id:
            data.pop("is_following", None)  # Remove o campo caso seja o próprio usuário

        return data