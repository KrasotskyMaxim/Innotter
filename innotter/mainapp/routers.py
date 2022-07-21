from email.mime import base
from django.db import router
from rest_framework import routers

from .views import *


pages_router = routers.DefaultRouter()
pages_router.register(r"pages", PageViewSet, basename="pages")

tags_router = routers.DefaultRouter()
tags_router.register(r"tags", TagViewSet, basename="tags")

posts_router = routers.DefaultRouter()
posts_router.register(r"posts", PostViewSet, basename="posts")
