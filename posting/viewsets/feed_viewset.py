from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posting.models import Post
from posting.serializers import PostSerializer

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        following = user.following.all()

        posts = (
            Post.objects
            .filter(user__in=following)
            .exclude(post_type="COMMENT")
            .order_by("-created_at")
        )

        serializer = PostSerializer(posts, many=True, context={"request": request})

        return Response(serializer.data)
