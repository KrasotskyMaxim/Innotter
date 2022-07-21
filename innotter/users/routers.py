from rest_framework import routers

from .views import *


users_router = routers.DefaultRouter()
users_router.register(r"users", UserViewSet, basename="users")
