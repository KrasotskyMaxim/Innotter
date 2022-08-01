from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status 
from rest_framework.permissions import IsAuthenticated
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
                                 ActionTagSerializer,
                                 PostFeedSerializer)
from mainapp.utils import (get_active_pages, 
                           get_blocked_pages, 
                           get_posts,
                           get_permission_list,
                           get_page_followers,
                           follow_page,
                           unfollow_page,
                           get_page_follow_requests,
                           accept_request,
                           deny_request,
                           accept_all_requests,
                           deny_all_requests,
                           get_page_tags,
                           add_tag,
                           remove_tag,
                           like_post,
                           unlike_post,
                           get_liked_posts,
                           get_follow_posts)
from users.permissions import IsAdmin, IsModerator, IsUser, IsBlockedUser


class PageViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    
    action_permission_classes = {
        "list": (IsAuthenticated, ~IsBlockedUser),
        "retrieve": (IsAuthenticated, ~IsBlockedUser),
        "update": (IsAuthenticated, IsAdmin | IsModerator),
        "partial_update": (IsAuthenticated, IsAdmin | IsModerator),
        "blocked": (IsAuthenticated, IsAdmin | IsModerator),
        "followers": (IsAuthenticated, ~IsBlockedUser),
        "follow": (IsAuthenticated, ~IsBlockedUser),
        "unfollow": (IsAuthenticated, ~IsBlockedUser),
    }

    detail_serializer_classes = {
        "admin": AdminPageDetailSerializer,
        "moderator": ModeratorPageDetailSerializer,
        "user": PageDetailSerializer,
    }
    
    list_serializer_classes = {
        "list": PageListSerializer,
        "blocked": PageListSerializer,
        "followers": FollowerListSerializer,
    }
    
    @action(detail=False, methods=["get"], url_path="blocked")
    def blocked(self, request):
        blocked_pages = get_blocked_pages()
        serializer = self.get_serializer(blocked_pages, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"], url_path="followers")
    def followers(self, request, pk=None):
        page_followers = get_page_followers(page_pk=pk, with_blocked=True)
        serializer = FollowerListSerializer(page_followers, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)       
    
    @action(detail=True, methods=["post"], url_path="follow") 
    def follow(self, request, pk=None):
        if not follow_page(user=self.request.user, page_pk=pk):
            return Response({"detail": "You have already been a subscriber!"}, status=status.HTTP_200_OK)
        
        return Response({"detail": "You apply for a subscription!"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow(self, request, pk=None):
        if not unfollow_page(user=self.request.user, page_pk=pk):
            return Response( {"detail": "You have already been unsubscribed!"}, status=status.HTTP_200_OK)
            
        return Response({"detail": "You unsubscribe from the page!"}, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        if self.request.user.role in ("admin", "moderator"):
            return Page.objects.all().order_by("id")
        
        return get_active_pages(is_owner_page=False)
    
    def get_serializer_class(self):
        if self.action in ("retrieve", "update", "partial_update", "follow", "unfollow"):
            return self.detail_serializer_classes.get(self.request.user.role)
        
        return self.list_serializer_classes.get(self.action)
    
    def get_permissions(self):
        return get_permission_list(self, permission_dict=self.action_permission_classes)
    

class OwnerPageViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    permission_classes = (IsAuthenticated, ~IsBlockedUser)
    
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
    
    @action(detail=True, methods=["get"], url_path="followers")
    def followers(self, request, pk=None):
        page_followers = get_page_followers(page_pk=pk)
        serializer = FollowerListSerializer(page_followers, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="follow-requests")
    def page_follow_requests(self, request, pk=None):
        follow_requests = get_page_follow_requests(page_pk=pk)
        serializer = FollowerListSerializer(follow_requests, many=True)
        serializer.is_valid(raise_exception=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="accept-request")
    def accept_follow_request(self, request, pk=None):
        serializer = FollowerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        
        if not accept_request(follower_email=email, page_pk=pk):
            return Response({"detail": "User is already your follower!"}, status=status.HTTP_200_OK)    
        
        return Response({"detail": "You successfully accept user to followers!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="deny-request")
    def deny_follow_request(self, request, pk=None):
        serializer = FollowerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        
        if not deny_request(follower_email=email, page_pk=pk):
            return Response({"detail": "User is already removed!"}, status=status.HTTP_200_OK)
        
        return Response({"detail": "You successfully remove user from followers!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="accept-all-requests")
    def accept_all_follow_requests(self, request, pk=None):
        if not accept_all_requests(page_pk=pk):
            return Response({"detail": "You don't hane follow requests!"}, status=status.HTTP_200_OK)

        return Response({"detail": "You successfully accept all follow requests!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="deny-all-requests")
    def deny_all_follow_requests(self, request, pk=None):
        if not deny_all_requests(page_pk=pk):
            return Response({"detail": "You don't have follow requests!"}, status=status.HTTP_200_OK)

        return Response({"detail": "You successfully deny all follow requests!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="tags")
    def tags(self, request, pk=None):
        page_tags = get_page_tags(page_pk=pk)
        serializer = TagSerializer(page_tags, many=True)
        serializer.is_valid(raise_exception=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="add-tag")
    def add_tag_to_page(self, request, pk=None):
        serializer = ActionTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag_name = serializer.validated_data.get("name")
        
        if not add_tag(tag_name=tag_name, page_pk=pk):
            return Response({"detail": "Tag already added!"}, status=status.HTTP_200_OK)    
        
        return Response({"detail": "You have successfully added tag to page!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], url_path="remove-tag")
    def remove_tag_from_page(self, request, pk=None):
        serializer = ActionTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag_name = serializer.validated_data.get("name")
        
        if not remove_tag(tag_name=tag_name, page_pk=pk):
            return Response({"detail": "Tag already removed!"}, status=status.HTTP_200_OK)
                
        return Response({"detail": "You have successfully removed tag from page!"}, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        return get_active_pages(is_owner_page=True, owner=self.request.user)
    
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, UserPageDetailSerializer)
    

class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all().order_by("id")
    permission_classes = (IsAuthenticated, IsAdmin | IsModerator, ~IsBlockedUser)
    serializer_class = PostListSerializer
    

class OwnerPostViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    permission_classes = (IsAuthenticated, ~IsBlockedUser)

    def get_queryset(self):
        return get_posts(is_owner_posts=True, owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ("retrieve", "update", "partial_update"):
            return PostDetailSerializer
        
        return PostListSerializer
    
    
class PostFeedViewSet(mixins.RetrieveModelMixin, 
                      mixins.ListModelMixin, 
                      GenericViewSet):
    serializer_class = PostFeedSerializer
    permission_classes = (IsAuthenticated, ~IsBlockedUser)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        if not like_post(user=self.request.user, post_pk=pk):
            return Response({"detail": "You already liked this post!"}, status=status.HTTP_200_OK)
        
        return Response({"detail": "You like post!"})

    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk=None):
        if not unlike_post(user=self.request.user, post_pk=pk):
            return Response({"detail": "You already unliked this post!"}, status=status.HTTP_200_OK)
        
        return Response({"detail": "You unlike post!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="liked")
    def liked(self, request, pk=None):
        liked_posts = get_liked_posts(user=self.request.user)
        serializer = self.get_serializer(liked_posts, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return get_follow_posts(user=self.request.user)
    
    
class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, ~IsBlockedUser)
    
    action_permission_classes = {
        "list": (IsAuthenticated, ~IsBlockedUser),
        "create": (IsAuthenticated, ~IsBlockedUser),
        "destroy": (IsAuthenticated, IsAdmin | IsModerator, ~IsBlockedUser),
    }

    def get_permissions(self):
        return get_permission_list(self, permission_dict=self.action_permission_classes)
    