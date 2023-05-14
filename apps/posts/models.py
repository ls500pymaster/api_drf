from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	content = models.TextField(
		blank=True,
		null=False
	)
	created_at = models.DateTimeField(
		auto_now_add=True
	)

	def __str__(self):
		return self.content

	class Meta:
		ordering = ["-created_at"]


class PostLike(models.Model):
	post = models.ForeignKey(
		Post,
		related_name="likes",
		on_delete=models.CASCADE,
		null=True
	)
	user = models.ForeignKey(
		User,
		related_name="liked_posts",
		on_delete=models.CASCADE,
		null=True
	)
	liked_at = models.DateTimeField(
		auto_now_add=True
	)

	class Meta:
		unique_together = ("user", "post",)

	def __str__(self):
		return f"{self.post.id} liked by {self.user.first_name} at {self.liked_at}"
