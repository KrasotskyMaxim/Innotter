from rest_framework import serializers

from mainapp.models import Page, Post, Tag


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        # fields = "__all__"
        fields = ("id", "name", "uuid", "description", "image", "is_private", "tags", "is_blocked", "owner", "followers", "follow_requests", "unblock_date")
        

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "page", "content", "reply_to", "created_at", "updated_at")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
