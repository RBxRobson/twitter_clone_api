from rest_framework import serializers
from accounts.models import User

class UserDetailSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'profile']

    # Adiciona o profile no retorno
    def get_profile(self, instance):
            return {
                'bio': instance.profile.bio,
                'avatar': instance.profile.avatar.url,
                'header': instance.profile.header.url
            }
