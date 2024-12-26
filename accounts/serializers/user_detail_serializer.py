from rest_framework import serializers
from accounts.models import User

class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'profile', 'followers_count', 'following_count', 'created_at', 'updated_at']

    def get_profile(self, instance):
        return {
            'bio': instance.profile.bio,
            'avatar': instance.profile.avatar.url,
            'header': instance.profile.header.url,
            'updated_at': instance.profile.updated_at
        }

    def get_followers_count(self, instance):
        return instance.followers.count()

    def get_following_count(self, instance):
        return instance.following.count()
