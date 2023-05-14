from rest_framework import serializers
from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
	class Meta:
		models = PostLike
		fields = "__all__"
