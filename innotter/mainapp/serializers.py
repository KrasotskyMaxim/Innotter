from rest_framework import serializers

from mainapp.models import Page, Post, Tag


class PageListSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
     
    class Meta:
        model = Page
        fields = ("id", "name", "uuid", "owner", "is_private", "is_blocked")
        
        
class PageDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username", allow_null=True)

    class Meta:
        model = Page
        fields = ("name", "uuid", "description", "tags", "owner", "followers", "is_private")
        read_only_fields = ("name", "uuid", "description", "tags", "owner", "followers", "is_private")
      
        
class UserPageDetailSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username")
    follow_requests = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username")
    tags = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Tag.objects.all())
    is_private = serializers.BooleanField(required=True)

    class Meta:
        model = Page
        fields = ("id", "name", "uuid", "description", "tags", "owner", "image_s3_path", "followers", "is_private", "follow_requests")
        read_only_fields = ("followers", "follow_requests")


class AdminPageDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username", allow_null=True)
    is_blocked = serializers.BooleanField()

    class Meta:
        model = Page
        fields = ("id", "name", "uuid", "description", "tags", "owner", "image_s3_path", "followers", "is_private", "unblock_date", "is_blocked")
        read_only_fields = ("id", "name", "uuid", "description", "tags", "owner", "image_s3_path", "followers", "is_private")


class ModeratorPageDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username", allow_null=True)
    unblock_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Page
        fields = ("id", "name", "uuid", "description", "tags", "owner", "image_s3_path", "followers", "is_private", "unblock_date", "is_blocked")
        read_only_fields = ("id", "name", "uuid", "description", "tags", "owner", "image_s3_path", "followers", "is_private", "is_blocked")


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "page", "content", "reply_to", "created_at", "updated_at")


class PostDetailSerializer(serializers.ModelSerializer):
    page_name = serializers.SerializerMethodField()
    reply_to_content = serializers.SerializerMethodField(allow_null=True)
    likers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username")
    
    class Meta:
        model = Post
        fields = ("id", "content", "page", "page_name", "reply_to", "reply_to_content", "created_at", "updated_at", "likers")
        read_only_fields = ("page", "created_at", "updated_at", "likers")
        
    def get_page_name(self, post):
        return post.page.name

    def get_reply_to_content(self, post):
        return post.reply_to.content if post.reply_to else None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
