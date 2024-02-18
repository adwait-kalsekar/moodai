from django.shortcuts import render

# Create your views here.

def index(request):
    page = "home"

    context = { "page": page }
    return render(request, "base/index.html", context)

def about(request):
    page = "about"

    context = { "page": page }
    return render(request, "base/about.html", context)