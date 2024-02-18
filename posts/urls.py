from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("explore/", views.view_posts, name="view-posts"),
    path("upload/", views.upload_post, name="upload-post"),
    path("confirm_upload/", views.confirm_upload, name="confirm-upload"),
    path("post/<str:id>/", views.single_post, name="single-post"),
]