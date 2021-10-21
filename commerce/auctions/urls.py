from django.urls import path
from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("customer", views.customer, name="customer"),

    path("<int:listing_id>", views.listing, name="listing"),
    

    path("category", views.category, name="category"),
    path("bid", views.bid, name="bid"),

    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/addToWatchlist", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<str:pk>/", views.removeFromWatchlist, name="removeFromWatchlist"),

    path("myListing", views.my_listing, name="myListing"),
    path("add", views.add, name="add"),
    path("update_mylisting/<str:pk>/", views.updateMyListing, name="update_mylisting"),
    path("delete_mylisting/<str:pk>/", views.deleteMyListing, name="delete_mylisting"),
]
