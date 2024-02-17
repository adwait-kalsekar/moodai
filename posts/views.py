from django.shortcuts import render

# Create your views here.

def index(request):
    context = { "page": "home" }
    return render(request, "posts/index.html", context)