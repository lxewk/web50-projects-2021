from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.datetime_safe import date

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500, blank=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    highest_bid = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    listing_url = models.URLField(max_length=64, blank=True)
    category = models.CharField(max_length=64, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} current price is {self.current_price}"


class Comment_Auction_Listing(models.Model):
    comment_text = models.TextField(max_length=500, blank=True)
    like_count = models.IntegerField(default=0)


class Watchlist(models.Model):
    listed_items = models.ManyToManyField(Listing, blank=True)


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)


class User(AbstractUser):
    joined_on = models.DateField(default=date.today)
    listings = models.ManyToManyField(Listing, blank=True, related_name="users")
    comments = models.ManyToManyField(Comment_Auction_Listing, blank=True, related_name="users_comments")
    listing_creator = models.BooleanField(default=False)
    
    def __str__(self):
        return f"username: {self.username} - joined on: {self.joined_on}"


class Bid(models.Model):
    LEAST_AS_LARGE_STARTINGBID = 'LALS'
    GREATER_THAN_OTHER = 'GTO'
    ERROR_MESSAGE = [
        (LEAST_AS_LARGE_STARTINGBID, 'Your bid must be at least as large as the startingbid.'),
        (GREATER_THAN_OTHER, 'Your bid does not exceed existing bid!'),
    ]
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    placed_bid = models.DecimalField(max_digits=6, decimal_places=2)
    highest_bidder = models.OneToOneField(User, on_delete=models.CASCADE)
    bid_error = models.CharField(
        max_length=100,
        error_messages = ERROR_MESSAGE
    )

    def __str__(self):
        return f"starting bid:{self.starting_bid} - placed bid:{self.placed_bid} - highest bidder: {self.highest_bidder}"
