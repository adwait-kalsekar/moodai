from django.shortcuts import render, redirect

from .models import Post

# Create your views here.

def index(request):
    page = "home"

    context = { "page": page }
    return render(request, "posts/index.html", context)

def view_posts(request):
    page = "explore"

    context = { "page": page }
    return render(request, "posts/explore.html", context)

def upload_post(request):
    page = "upload"
    context = { "page": page }

    if request.method == "POST":
        prompt = request.POST["prompt"]
        print(prompt)
        context["prompt"] = prompt

    return render(request, "posts/upload.html", context)

def confirm_upload(request):
    post = Post()
    post.title = request.POST["title"]
    post.caption = request.POST["caption"]
    post.image_url = "static/assets/images/generated.png"
    return render(request, "posts/confirm_upload.html")

def single_post(request, id):
    return render(request, "posts/single_post.html")