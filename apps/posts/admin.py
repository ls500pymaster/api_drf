from django.contrib import admin
from .models import Post, PostLike


class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeInline]
