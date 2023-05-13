from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField(blank=True, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True, null=True)

	def __str__(self):
		return self.content

	class Meta:
		ordering = ["-created_at"]

# class Like(models.Model):
# 	user
# 	like


