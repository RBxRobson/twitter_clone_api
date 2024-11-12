from rest_framework import serializers
from accounts.models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'header']
