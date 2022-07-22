from email.mime import base
from django.db import router
from rest_framework import routers

from mainapp.views import PageViewSet, TagViewSet, PostViewSet


router = routers.DefaultRouter()

router.register(r"pages", PageViewSet, basename="pages")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"posts", PostViewSet, basename="posts")
