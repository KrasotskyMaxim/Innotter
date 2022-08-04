from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from mainapp.models import Page, Post, Tag 
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

def get_page_followers(page_pk: int, with_blocked: bool = False) -> Page:
    page = get_object_or_404(Page, pk=page_pk)
    
    if with_blocked:
        return page.followers.all().order_by("id")
    else:
        return page.followers.filter(is_blocked=False).order_by("id")
    

def get_page_follow_requests(page_pk: int) -> Page:
    page = get_object_or_404(Page, pk=page_pk)
    follow_requests = page.follow_requests.all().order_by("id")
    
    return follow_requests

def follow_page(user: User, page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    
    if page.followers.contains(user):
        return False 
    
    page.followers.add(user)
    
    return True
    

def unfollow_page(user: User, page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    if not page.followers.contains(user):
        return False     
    
    page.followers.remove(user)
    
    return True


def accept_request(follower_email: str, page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    follower = get_object_or_404(User, email=follower_email)
    
    if not page.follow_requests.contains(follower):
        return False
    
    page.followers.add(follower)
    page.follow_requests.remove(follower)
    
    return True


def deny_request(follower_email: str, page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    follower = get_object_or_404(User, email=follower_email)
    
    if not page.follow_requests.contains(follower):
        return False
    
    page.follow_requests.remove(follower)
    
    return True

def accept_all_requests(page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    follow_requests = page.follow_requests.all()
    
    if not follow_requests:
        return False
    
    for follower in follow_requests:
        page.followers.add(follower)
        page.follow_requests.remove(follower)
        
    return True 

def deny_all_requests(page_pk: int):
    page = get_object_or_404(Page, pk=page_pk)
    follow_requests = page.follow_requests.all()
    
    if not follow_requests:
        return False
    
    for follower in follow_requests:
        page.follow_requests.remove(follower)
        
    return True
        

def get_posts(is_owner_posts: bool, owner=None) -> Post:
    pages = Page.objects.filter(
        Q(is_blocked=False), 
        Q(unblock_date__isnull=True) | Q(unblock_date__lt=timezone.now())
    )

    if is_owner_posts:
        pages = pages.filter(owner=owner)

    return Post.objects.filter(page__in=pages).order_by("id")

def get_follow_posts(user: User) -> Post:
    pages = Page.objects.filter(Q(followers=user) | Q(owner=user)).distinct()
    
    return Post.objects.filter(page__in=pages).order_by("-created_at")

    
def get_liked_posts(user: User) -> Post:
    return Post.objects.filter(likers=user).order_by("created_at")

def like_post(user: User, post_pk: int) -> bool:
    post = get_object_or_404(Post, pk=post_pk)
    
    if post.likers.contains(user):
        return False 
    
    post.likers.add(user)
    
    return True
    
    
def unlike_post(user: User, post_pk: int) -> bool:
    post = get_object_or_404(Post, pk=post_pk)
    
    if not post.likers.contains(user):
        return False    
    
    post.likers.remove(user)
    
    return True
    

def get_page_tags(page_pk: int) -> Tag:
    page = get_object_or_404(Page, pk=page_pk)
    
    return page.tags.all() 


def add_tag(tag_name: str, page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    tag = get_object_or_404(Tag, name=tag_name)
    
    if page.tags.contains(tag):
        return False
    
    page.tags.add(tag)
    
    return True 

def remove_tag(tag_name: str, page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    tag = get_object_or_404(Tag, name=tag_name)
    
    if not page.tags.contains(tag):
        return False
    
    page.tags.remove(tag)
    
    return True 

def get_send_email_data(page_pk: int):
    page = get_object_or_404(Page, pk=page_pk)
    page_followers = page.followers.filter(is_blocked=False)
    
    return page.name, [follower.email for follower in page_followers]
