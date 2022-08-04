from email.mime import base
from django.db import router
from rest_framework import routers

from mainapp.views import (PageViewSet, 
                           TagViewSet, 
                           PostViewSet, 
                           OwnerPageViewSet, 
                           OwnerPostViewSet,
                           PostFeedViewSet)


router = routers.DefaultRouter()

router.register(r"pages", PageViewSet, basename="pages")
router.register(r"owner-pages", OwnerPageViewSet, basename="owner-pages")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"owner-posts", OwnerPostViewSet, basename="owner-posts")
router.register(r"feed", PostFeedViewSet, basename="feed")
