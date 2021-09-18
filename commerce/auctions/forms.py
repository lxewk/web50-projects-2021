from django import forms
from django.db.models import fields
from .models import Listing

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'current_price', 'listing_url', 'category')
        widget = {
            'title': form.TextInput(attrs={'class': 'form-control'}),
            'description': form.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'current_price': form.Number(attrs={'class': 'form-control'}),
            'listing_url': form.TextInput(attrs={'class': 'form-control'}),
            'category': form.Select(attrs={'class': 'form-control'}),

        }