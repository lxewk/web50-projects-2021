from django.contrib import admin

from .models import User, Bid, Listing, Watchlist, Category, Customer

# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Customer)