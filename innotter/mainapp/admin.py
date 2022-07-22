from django.contrib import admin

from mainapp.models import Post, Page, Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "page", "reply_to", "updated_at")
    list_display_links = ("id", "content")


class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "uuid", "is_blocked", "is_private", "owner")
    list_display_links = ("id", "name")


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


admin.site.register(Tag)
admin.site.register(Page)
admin.site.register(Post)
