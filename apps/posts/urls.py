from django.urls import include
from django.urls import path

from .views import Post, PostCreateView, LikeUnlikePostView, PostLikesAnalyticView

app_name = "posts"

urlpatterns = [
	path("create/", PostCreateView.as_view(), name="post_create"),
	path("<int:pk>/like/", LikeUnlikePostView.as_view(), name="post_likes"),
	path("analytics/", PostLikesAnalyticView.as_view(), name="analytics"),
]