from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.posts.models import Post, PostLike
from .serializers import PostSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeUnlikePostView(APIView):

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get("pk")
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        post_like = PostLike.objects.filter(user=user, post=post)

        if post_like.exists():
            post_like.delete()
        else:
            PostLike.objects.create(user=user, post=post)
            message = "Post Liked"

        post_serializer = PostSerializer(post)
        return Response({
            "message": message,
            "post": post_serializer.data
        }, status=status.HTTP_200_OK)


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
            likes_count=Count("likes")
        ).order_by("date")

        return Response(data=queryset)