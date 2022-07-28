from django.db.models import Q
from django.utils import timezone

from mainapp.models import Page, Post
from users.models import User


def get_permission_list(self, permission_dict: dict) -> list:
    permission_classes = permission_dict.get(self.action, list())
    
    return [permission() for permission in permission_classes]

def get_active_pages(is_owner_page: bool, owner=None) -> Page:
    pages = Page.objects.filter(
        Q(is_blocked=False),
        Q(unblock_date__isnull=True) | Q(unblock_date__lt=timezone.now()),
    ).order_by("id")
    
    if is_owner_page:
        pages = pages.filter(owner=owner)
    
    return pages

def get_blocked_pages() -> Page:
    return Page.objects.filter(is_blocked=True).order_by("id")

def get_posts(is_owner_posts: bool, owner=None) -> Post:
    pages = Page.objects.filter(
        Q(is_blocked=False), 
        Q(unblock_date__isnull=True) | Q(unblock_date__lt=timezone.now())
    )

    if is_owner_posts:
        pages = pages.filter(owner=owner)

    return Post.objects.filter(page__in=pages).order_by("id")

def get_liked_posts(user: User) -> Post:
    return Post.objects.filter(likers=user).order_by("created_at")
