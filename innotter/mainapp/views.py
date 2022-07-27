from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action 
from rest_framework.response import Response

from mainapp.models import Page, Post, Tag
from mainapp.serializers import PageDetailSerializer, PageListSerializer, PostDetailSerializer, \
    PostListSerializer, TagSerializer, UserPageDetailSerializer
from mainapp.utils import get_active_pages, get_blocked_pages, get_posts


class PageViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    permission_classes = (IsAuthenticated,)
    
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
    

class OwnerPageViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    permission_classes = (IsAuthenticated,)
    
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
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.action in ("retrieve", "update"):
            return PostDetailSerializer
        
        return PostListSerializer
    

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
    