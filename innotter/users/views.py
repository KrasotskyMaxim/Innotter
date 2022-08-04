from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.decorators import action

from users.models import User
from users.serializers import (UserListSerializer, 
                               UserDetailSerializer, 
                               UserRegistrationSerializer,
                               UserLoginSerializer, 
                               UserRefreshSerializer,
                               UserProfileSerializer)
from users.permissions import IsAdmin, IsNotBlockedUser
from users.utils import (block_or_unblock_owner_pages, 
                         access_to_admin_panel,
                         update_user_avatar)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if "is_blocked" in request.data:
            block_or_unblock_owner_pages(user=instance)
        
        if "role" in request.data:
            access_to_admin_panel(user=instance)
            
        return Response(serializer.data) 
    
        
    def get_serializer_class(self):
        if self.action in ["retrieve", "update"]:
            return UserDetailSerializer
        
        return UserListSerializer
    
    
class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    
    permission_classes = (IsAuthenticated, IsNotBlockedUser)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)
    
    @action(detail=True, methods=["put"])
    def set_avatar(self, request, pk):
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

        data, stat = update_user_avatar(request, pk)
        return Response(
            data=data,
            status=stat
        )
    
    

class UserRegistrationViewSet(mixins.CreateModelMixin,
                              GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    
    
class UserLoginViewSet(mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
    

class RefreshLoginViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRefreshSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)