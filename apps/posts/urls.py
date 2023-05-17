from django.urls import path

from .views import PostCreateView, LikeUnlikePostView, PostLikesAnalyticView, PostListView

app_name = "posts"

urlpatterns = [
	path("all/", PostListView.as_view(), name="post_list"),
	path("create/", PostCreateView.as_view(), name="post_create"),
	path("<int:pk>/like/", LikeUnlikePostView.as_view(), name="post_likes"),
	path("analytics/", PostLikesAnalyticView.as_view(), name="analytics"),
]