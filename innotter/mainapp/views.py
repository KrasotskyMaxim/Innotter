from django.shortcuts import render

from rest_framework import viewsets

from .models import *
from .serializers import *


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    
    def get_queryset(self):
        return Page.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.all()
    
    
class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    
    def get_queryset(self):
        return Tag.objects.all()
    