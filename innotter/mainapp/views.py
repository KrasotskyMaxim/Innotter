from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action 
from rest_framework.response import Response

from mainapp.models import Page, Post, Tag
from mainapp.serializers import (AdminPageDetailSerializer, 
                                 PageDetailSerializer, 
                                 PageListSerializer, 
                                 PostDetailSerializer,
                                 PostListSerializer, 
                                 TagSerializer, 
                                 UserPageDetailSerializer, 
                                 FollowerListSerializer,
                                 FollowerSerializer,
                                 AdminPageDetailSerializer,
                                 ModeratorPageDetailSerializer,
                                 ActionTagSerializer)
from mainapp.utils import (get_active_pages, 
                           get_blocked_pages, 
                           get_posts,
                           get_permission_list)
from users.permissions import IsAdmin, IsModerator, IsUser


class PageViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    
    action_permission_classes = {
        "list": (IsAuthenticated,),
        "retrieve": (IsAuthenticated,),
        "update": (IsAuthenticated, IsAdmin, IsModerator),
        "partial_update": (IsAuthenticated, IsAdmin, IsModerator),
        "blocked": (IsAuthenticated, IsAdmin, IsModerator),
        "followers": (IsAuthenticated,),
        "follow": (IsAuthenticated,),
        "unfollow": (IsAuthenticated,),
    }

    list_serializer_classes = {
        "list": PageListSerializer,
        "blocked": PageListSerializer,
        "followers": FollowerListSerializer,
    }

    detail_serializer_classes = {
        "admin": AdminPageDetailSerializer,
        "moderator": ModeratorPageDetailSerializer,
        "user": PageDetailSerializer,
    }
    
    @action(detail=False, methods=["get"], url_path="blocked")
    def blocked(self, request):
        all_blocked_pages = get_blocked_pages()
        serializer = self.get_serializer(all_blocked_pages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        if self.request.user.role in ("admin", "moderator"):
            return Page.objects.all().order_by("id")
        
        return get_active_pages(is_owner_page=False)
    
    def get_serializer_class(self):
        if self.action in ("retrieve", "update"):
            return PageDetailSerializer
        
        return PageListSerializer
    
    def get_permissions(self):
        return get_permission_list(self, permission_dict=self.action_permission_classes)
    

class OwnerPageViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    permission_classes = (IsAuthenticated,)
    
    serializer_classes = {
        "list": PageListSerializer,
        "create": PageListSerializer,
        "page_follow_requests": FollowerListSerializer,
        "all_follow_requests": FollowerListSerializer,
        "followers": FollowerListSerializer,
        "deny_follow_request": FollowerSerializer,
        "accept_follow_request": FollowerSerializer,
        "tags": TagSerializer,
        "add_tag_to_page": ActionTagSerializer,
        "remove_tag_from_page": ActionTagSerializer,
    }
    
    def get_queryset(self):
        return Page.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ("retrieve", "update"):
            return UserPageDetailSerializer
        
        return PageListSerializer
    

class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all().order_by("id")
    permission_classes = (IsAuthenticated, IsAdmin, IsModerator)
    

class OwnerPostViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_posts(is_owner_posts=True, owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ("retrieve", "update"):
            return PostDetailSerializer
        
        return PostListSerializer
    
    
class TagViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)
    
    action_permission_classes = {
        "list": (IsAuthenticated,),
        "create": (IsAuthenticated,),
        "destroy": (IsAuthenticated, IsAdmin, IsModerator),
    }

    def get_permissions(self):
        return get_permission_list(self, permission_dict=self.action_permission_classes)
    