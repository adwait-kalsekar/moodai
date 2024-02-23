import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.views.decorators.csrf import csrf_exempt

from .models import Profile
from posts.models import Post

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

@csrf_exempt
def login(request):
    if "auth0_user" in request.session:
        return redirect('view-posts')
    
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def profile(request):
    page = "profile"

    if not "auth0_user" in request.session:
        return redirect('home')
    
    context = { "page": page, "user": request.session["auth0_user"] }
    
    try:
        profile = Profile.objects.get(email=request.session["auth0_user"]["userinfo"]["email"])
        posts = Post.objects.filter(user=profile).order_by('-created')
        context["user_profile"] = profile
        context["posts"] = posts
        context["num_posts"] = len(posts)

    except Exception as err:
        print("Error: ", err)
        return render(request, "error.html")

    
    return render(request, "users/profile.html", context)

@csrf_exempt
def edit_profile(request):
    page = "edit-profile"

    if not "auth0_user" in request.session:
        return redirect('home')

    
    try:
        profile = Profile.objects.get(email=request.session["auth0_user"]["userinfo"]["email"])

        if request.method == "POST":
            if request.POST["name"]:
                profile.name = request.POST["name"]
            if request.POST["username"]:
                profile.username = request.POST["username"]

            profile.save()
            return redirect("user-profile")

        context = { "page": page, "user": request.session["auth0_user"], "user_profile": profile }
        return render(request, "users/edit.html", context)

    except Exception as err:
        print("Error: ", err)
        return render(request, "error.html")

@csrf_exempt
def view_all_users(request):
    page = "users"
    try:
        if "auth0_user" in request.session:
            users = Profile.objects.exclude(email=request.session["auth0_user"]["userinfo"]["email"])

        else:
            users = Profile.objects.all()
        

        context = { "page": page, "users": users }

        return render(request, "users/all_users.html", context)
    
    except Exception as err:
        print("Error: ", err)
        return render(request, "error.html")

def render_error(request, all_paths):
    return render(request, "error404.html")