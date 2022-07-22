from django.urls import include, path

from mainapp.routers import router


urlpatterns = [
    path("", include(router.urls)),
]
