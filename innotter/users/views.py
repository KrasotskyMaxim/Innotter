from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from users.models import User
from users.serializers import UserListSerializer, UserDetailSerializer, UserRegistrationSerializer, \
    UserLoginSerializer, UserRefreshSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    
    
    def get_serializer_class(self):
        if self.action in ["retrieve", "update"]:
            return UserDetailSerializer
        
        return UserListSerializer
    

class UserRegistrationViewSet(mixins.CreateModelMixin,
                              GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    
    
class UserLoginViewSet(mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    

class RefreshLoginViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRefreshSerializer
    