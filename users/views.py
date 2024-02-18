import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

from .models import Profile

# OAuth Setup
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

# Create your views here.


def index(request):
    return redirect(reverse("home"))

def login(request):
    if "user" in request.session:
        return redirect('home')
    
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["auth0_user"] = token

    try:
        profile = Profile.objects.get(email=token["userinfo"]["email"])
        return redirect(request.build_absolute_uri(reverse("index")))

    except Exception as err:
        print("Error: ", err)

    profile = Profile()
    profile.name = token["userinfo"]["name"]
    profile.email = token["userinfo"]["email"]
    profile.username = token["userinfo"]["nickname"]
    profile.save()
    print("Profile Created")

    print(token["userinfo"]["email"])
    return redirect(request.build_absolute_uri(reverse("index")))

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def profile(request):
    page = "profile"

    if not "auth0_user" in request.session:
        return redirect('home')
    
    try:
        profile = Profile.objects.get(email=request.session["auth0_user"]["userinfo"]["email"])
        user_profile = { "email": profile.email, "username": profile.username, "name": profile.name }

    except Exception as err:
        print("Error: ", err)
        return render(request, "error.html")

    context = { "page": page, "user": request.session["auth0_user"], "user_profile": user_profile }
    return render(request, "users/profile.html", context)

def edit_profile(request):
    page = "edit-profile"

    if not "auth0_user" in request.session:
        return redirect('home')

    
    try:
        profile = Profile.objects.get(email=request.session["auth0_user"]["userinfo"]["email"])
        user_profile = { "email": profile.email, "username": profile.username, "name": profile.name }

        print(user_profile)

        if request.method == "POST":
            profile.name = request.POST["name"]
            profile.username = request.POST["username"]
            profile.save()
            user_profile = { "email": profile.email, "username": profile.username, "name": profile.name }
            print(user_profile)

        context = { "page": page, "user": request.session["auth0_user"], "user_profile": user_profile }
        return render(request, "users/edit.html", context)

    except Exception as err:
        print("Error: ", err)
        return render(request, "error.html")

