from rest_framework import serializers
from posting.models import Like
from django.contrib.contenttypes.models import ContentType

class LikeSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    object_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id', 'created_at']
        read_only_fields = ['id', 'created_at']
