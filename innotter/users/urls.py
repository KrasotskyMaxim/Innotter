from django.urls import include, path

from .routers import *


urlpatterns = [
    path("api/v1/", include(users_router.urls))
]