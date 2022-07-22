from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from mainapp.models import Page, Post, Tag
from mainapp.serializers import PageSerializer, PostSerializer, TagSerializer


class PageViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = PageSerializer
    
    queryset = Page.objects.all()
    

class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = PostSerializer
    
    queryset = Post.objects.all()
    
    
class TagViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = TagSerializer
    
    queryset = Tag.objects.all()
    