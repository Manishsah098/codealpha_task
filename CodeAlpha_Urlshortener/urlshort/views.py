from django.shortcuts import render, redirect, get_object_or_404
from .models import Url
from .utils import generate_short_url


def home(request):
    urls = Url.objects.all()
    return render(request, "home.html", {"urls": urls})


def shorten_url(request):
    if request.method == "POST":
        long_url = request.POST.get("long_url")
        short_url = generate_short_url()

        url = Url(long_url=long_url, short_url=short_url)
        url.save()

        return redirect("home")

    return render(request, "shorten_url.html")


def redirect_to_original(request, short_url):
    url = get_object_or_404(Url, short_url=short_url)
    return redirect(url.long_url)