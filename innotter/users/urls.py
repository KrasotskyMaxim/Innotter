from django.urls import include, path

from users.routers import router


urlpatterns = [
    path("", include(router.urls))
]