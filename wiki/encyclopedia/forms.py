from django import forms


class SearchEntryForm(forms.Form):
    entry = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Search Encyclopedia',
        }
    ))

class CreateEntryForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
        attrs= {
            'class': 'form-control',
            'placeholder': '#Title',
        }), 
        required=True,
        label=''
        
    )
    content = forms.CharField(
        widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter the Markdown content of the page.'
        }),
        required=True,
        label=''
    )