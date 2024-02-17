from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("posts.urls")),
    path("", include("users.urls")),
]
