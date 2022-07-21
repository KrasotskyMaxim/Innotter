from django.urls import include, path

from .routers import *


urlpatterns = [
    path("api/v1/", include(pages_router.urls)),
    path("api/v1/", include(tags_router.urls)),
    path("api/v1/", include(posts_router.urls)),
]
