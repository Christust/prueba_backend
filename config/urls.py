from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Apps
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("maestros/", include("apps.entidades.urls")),
]
