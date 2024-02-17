from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="user_home"),
    path("profile/<str:username>", views.profiles, name="user_profile")
]