from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework import generics, status
from rest_framework.response import Response
from apps.posts.models import Post
from .serializers import PostSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeUnlikePostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if user in post.liked_by.all():
            post.liked_by.remove(user)
        else:
            post.liked_by.add(user)

        return Response(self.get_serializer(post).data, status=status.HTTP_200_OK)


class PostLikesAnalyticView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if not all([date_from, date_to]):
            return Response(data={"error": "Both parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Post.objects.filter(
            created_at__range=[date_from, date_to]
        ).annotate(
            date=TruncDay("created_at")
        ).values("date").annotate(
            likes_count=Count("liked_by")
        ).order_by("date")

        return Response(data=queryset)