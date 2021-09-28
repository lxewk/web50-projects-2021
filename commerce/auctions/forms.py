from django import forms
from .models import Listing


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description',
                  'starting_bid', 'image_url', 'category', 'status']
        widgets = {
            'title': forms.TextInput(
				   attrs={'class': 'form-control'}),
            'description': forms.Textarea(
				   attrs={'class': 'form-control', 'row': '3'}),
            'starting_bid': forms.NumberInput(
				   attrs={'class': 'form-control'}),
            'category': forms.Select(
                attrs={'class': 'form-control'}),
            'status': forms.Select(
                attrs={'class': 'form-control'}
            )
        }


# Creating a form to add an listing
# form = CreateListingForm()

# Creating a form to change an existing listing
# listing = Listing.objects.get(pk=1)
# form = CreateListingForm(instance=listing)