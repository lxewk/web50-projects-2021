from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.datetime_safe import date

        
STATUS = [
    ('ACTIVE', 'Active'),
    ('NON_ACTIVE', 'Non-active')
]


class User(AbstractUser):
    first = models.CharField(max_length=64, null=True)
    last = models.CharField(max_length=64, null=True)
    birth_date = models.DateField(default=date.today, null=True)
    joined_on = models.DateField(default=date.today, null=True)
    
    def __str__(self):
        return f"username: {self.username} - joined on: {self.joined_on}"


class Category(models.Model):
    category_name = models.CharField(max_length=64, null=True)
    is_category = models.BooleanField(default=False)
    
    def __str__(self):
        return self.category_name



class Listing(models.Model):
    title = models.CharField(max_length=64, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    image_url = models.ImageField(blank=True, null=True, upload_to="images/")
    # Each Listing is related to one category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_category': True})

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    users = models.ManyToManyField(User, through='Watchlist')
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return f"{self.title} starting bid {self.starting_bid}  created {self.date_created}"

    @property
    def imageUrl(self):    
        if self.image_url and hasattr(self.image_url, 'url'):
            return self.image_url.url
        else:
            return "/media/images/noPhoto.jpeg"




class Comment_Auction_Listing(models.Model):
    comment_text = models.TextField(max_length=500, blank=True, null=True)
    like_count = models.IntegerField(default=0, null=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, blank=True, null=True)


class Bid(models.Model):
    LEAST_AS_LARGE_STARTINGBID = 'LALS'
    GREATER_THAN_OTHER = 'GTO'
    ERROR_MESSAGE = [
        (LEAST_AS_LARGE_STARTINGBID, 'Your bid must be at least as large as the startingbid.'),
        (GREATER_THAN_OTHER, 'Your bid does not exceed existing bid!'),
    ]
    start_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    placed_bid = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bid_error = models.CharField(
        max_length=100,
        error_messages = ERROR_MESSAGE,
        null=True
    )

    def __str__(self):
        return f"start price:{self.start_price} - placed bid:{self.placed_bid} - highest bidder: {self.highest_bidder}"
