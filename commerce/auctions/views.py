from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Customer, User, Listing, Watchlist
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
        first = request.POST["first"]
        last = request.POST["last"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, first=first, last=last, email=email, password=password)
            user.save()
            # Create Customer, one to one with user (own addition)
            Customer.objects.create(
                user = user,
                )
            # Add Watchlist to the user (own addition)
            Watchlist.objects.create(
                user = user,
            )
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
        


@login_required
def customer(request):
    user = request.user
    costumer = user.costumer
    
    
    return render(request, "auctions/watchlist.html", {
        "costumer": costumer,
    })



@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    customers = listing.customers.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "customers": customers,
    })




@login_required
def my_listing(request):
    return render(request, "auctions/myListing.html", {
        "listings": Listing.objects.filter(creator=request.user)
    })

@login_required
def add(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)

            # Add creator to the listing
            creator = request.user
            listing.creator = creator
            listing.save()
            creator.is_creator = True

            return HttpResponseRedirect(reverse("auctions:myListing"))

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
def updateMyListing(request, pk):
    listing = Listing.objects.get(id=pk)
    form = CreateListingForm(instance=listing)

    if request.method == "POST":
        form = CreateListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return render(request, "auctions/myListing.html")

        else:
            return render(request, "auctions/myListing.html", {
                "form": form
            })


@login_required
def deleteMyListing(request, pk):
    listing = Listing.objects.get(id=pk)
    if request.method == "POST":
        listing.delete()
        return render(request, "auctions/myListing.html")

    return render(request, "auctions/delete.html", {
         "listing": listing 
    })




@login_required
def watchlist(request):
    watchlist = Watchlist.objects.get(user=request.user)
    listings = watchlist.listing.all()
    total_listings = listings.count()
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "total_listings": total_listings
    })

@login_required
def addToWatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.follow == True:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(status='ACTIVE'),
            "message": "Item already on your watchlist."
        })   
    else:
        listing.follow = True
        listing.save()
        watchlist = Watchlist.objects.get(user=request.user)
        watchlist.listing.add(listing)

        return HttpResponseRedirect(reverse("auctions:watchlist")) 


@login_required
def removeFromWatchlist(request, pk):
    listing = Listing.objects.get(id=pk)
    listing.follow = False
    listing.save()

    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.listing.remove(listing)

    listings = watchlist.listing.all()
    total_listings = listings.count()
    
    return render(request, "auctions/watchlist.html", {
        "listing": listing,
        "listings": listings,
        "total_listings": total_listings,
        "message": "is removed from your watchlist."
    })




@login_required
def category(request):
    return render(request, "auctions/category.html")

@login_required
def bid(request):
    return render(request, "auctions/bid.html")