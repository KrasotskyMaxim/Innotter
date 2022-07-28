from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserListSerializer, UserDetailSerializer, UserRegistrationSerializer, \
    UserLoginSerializer, UserRefreshSerializer
from users.permissions import IsAdmin


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)
    
    def get_serializer_class(self):
        if self.action in ["retrieve", "update"]:
            return UserDetailSerializer
        
        return UserListSerializer
    

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