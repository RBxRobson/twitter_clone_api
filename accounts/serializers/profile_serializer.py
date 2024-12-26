from rest_framework import serializers
from accounts.models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'header']

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_header(self, obj):
        request = self.context.get('request')
        if obj.header and request:
            return request.build_absolute_uri(obj.header.url)
        return None
