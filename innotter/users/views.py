from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .models import *
from .serializers import *


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()