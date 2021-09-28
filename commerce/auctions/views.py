from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Listing
from .forms import CreateListingForm


def index(request):
    # Only the active listings
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status='ACTIVE')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
        

@login_required
def listing(request):
    if "my_listings" not in request.session:
        request.session["my_listings"] = []

    return render(request, "auctions/listing.html", {
        "listings": request.session["my_listings"]
    })



@login_required
def add(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("auctions:index"))

        # Form not valid, re-render the page with existing information
        else:
            return render(request, "auctions/add.html", {
            "form": form 
            })

    # If method is GET, render an empty Create form
    return render(request, "auctions/add.html", {
        "form": CreateListingForm()
    })
    

@login_required
def category(request):
    return render(request, "auctions/category.html")

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html")

@login_required
def bid(request):
    return render(request, "auctions/bid.html")