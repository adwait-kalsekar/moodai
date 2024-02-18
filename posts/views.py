from django.shortcuts import render, redirect
import requests
from django.conf import settings

from .models import Post
from .image_generator import generate_from_prompt
from users.models import Profile

# Create your views here.

def index(request):
    page = "home"

    context = { "page": page }
    return render(request, "posts/index.html", context)

def view_posts(request):
    page = "explore"

    newest_to_oldest = Post.objects.all().order_by('-created')

    all_posts = Post.objects.all()

    context = { "page": page, "recent_posts": newest_to_oldest, "all_posts": all_posts }
    return render(request, "posts/explore.html", context)

def upload_post(request):
    if not "auth0_user" in request.session:
        return redirect('login')
    
    page = "upload"
    context = { "page": page }

    if request.method == "POST":
        prompt1 = request.POST["prompt1"]
        prompt2 = request.POST["prompt2"]
        image_url = generate_from_prompt(prompt1, prompt2)
        print(image_url)
        request.session["image_url"] = image_url
        context["prompt1"] = prompt1
        context["prompt2"] = prompt2
        context["image_url"] = image_url

        fastapi_url = settings.FASTAPI_URL

        data = { "email": request.session["auth0_user"]["userinfo"]["email"], "prompt1": prompt1, "prompt2": prompt2, "image_url": image_url }
        
        try:
            # Send POST request to FastAPI endpoint
            response = requests.post(fastapi_url, json=data)

        except Exception as err:
            print("Error: ", err)
            print("Could not upload to MongoDB through FastAPI")


    return render(request, "posts/upload.html", context)

def confirm_upload(request):
    if not "auth0_user" in request.session:
        return redirect('login')

    if request.method == "POST":
        user_email = request.session["auth0_user"]["userinfo"]["email"]

        try:
            profile = Profile.objects.get(email=user_email)
            image_url = request.session["image_url"]
            post = Post()
            post.title = request.POST["title"]
            post.caption = request.POST["caption"]
            post.user = profile
            post.image_url = image_url
            post.save()

            profile.ai_credits -= 1
            profile.save()

        except Exception as err:
            print("Error: ", err)
            return render("error.html")
        

        del request.session["image_url"]

    return redirect("user-profile")

def single_post(request, id):
    return render(request, "posts/single_post.html")