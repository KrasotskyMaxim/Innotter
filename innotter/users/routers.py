from rest_framework import routers

from users.views import UserRegistrationViewSet, UserViewSet, UserLoginViewSet


router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"registration", UserRegistrationViewSet, basename="registration")
router.register(r"login", UserLoginViewSet, basename="login")
