import markdown2
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from . import util
from .forms import SearchEntryForm, CreateEntryForm, EditEntryForm
        


def index(request):
    if request.method == "POST":
        form = SearchEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            the_entries = util.list_entries()
            request.session["completeTitle"] = entry.casefold() in (string.casefold() for string in the_entries)
            request.session["sub"] = list(filter(lambda i: entry.casefold() in i, (string.casefold() for string in the_entries)))

            # complete title
            if request.session["completeTitle"] == True :  
                return HttpResponseRedirect(reverse("encyclopedia:get", args=[entry]))
            # substring of the title
            else:
                return HttpResponseRedirect(reverse("encyclopedia:search"))

        # Form not valid, re-render the page with existing information           
        else:
            return render(request, "encyclopedia/index.html", {
                "entryForm": form
            })
    # If method is GET , render the list of entries and an empty Search form
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "entryForm": SearchEntryForm()
    })


def get(request, title):
    try:
        title = title
        text = markdown2.markdown(util.get_entry(title))
        request.session["title"] = title

        return render(request, "encyclopedia/get.html", {
            "entry": text, 
            "title": title     
        })
    except TypeError:
        number = 404
        error = "Page not found"
        return render(request, "encyclopedia/exception.html", {
            "number": number,
            "error": error
        })
        

def search(request):
    subString = request.session["sub"]
    subString = [sub.capitalize() for sub in subString]
    
    return render(request, "encyclopedia/search.html", {
        "sub": subString
    })


def create(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            existing_entries = util.list_entries()
            request.session["existingEntry"] = title.casefold() in (string.casefold() for string in existing_entries)

            # If title not exists, save new entry, and redirect to the new page
            if request.session["existingEntry"] == False:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:get", args=[title]))
            else:
                number = 58
                error = "File already exists"
                return render(request, "encyclopedia/exception.html", {
                    "number": number,
                    "error": error
                })
        else:
            # Form not valid, re-render the page with existing information
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    # If method is GET , render empty Create form
    return render(request, "encyclopedia/create.html", {
        "createForm": CreateEntryForm()
    })
    
def edit(request):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = request.session["title"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:get", args=[title]))
        else:
            # Form not valid, re-render the page with existing information
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    else:
        # If method is GET , populate the form with the Markdown of the entry
        title = request.session["title"]
        f = default_storage.open(f"entries/{title}.md")
        mdFile = f.read().decode("utf-8")
        form = EditEntryForm({'content': mdFile})

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })

def randomPage(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)

    return HttpResponseRedirect(reverse("encyclopedia:get", args=[selected_page]))