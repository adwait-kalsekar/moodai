from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.callback, name="callback"),
    path("profile/edit/", views.edit_profile, name="edit-profile"),
    path("profile/", views.profile, name="user-profile"),
    path("connect/", views.view_all_users, name="all-users"),

    path("<path:all_paths>/", views.render_error, name="error-page"),
]