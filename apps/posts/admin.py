from django.contrib import admin
from .models import Post


@admin.register(Post)
class AdminPosts(admin.ModelAdmin):
    list_display = ("user", "content", "created_at",)

