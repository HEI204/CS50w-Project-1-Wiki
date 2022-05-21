from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import random, os
from . import util, forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Visiting different entry by '/wiki/{title}'
def entry(request, title):
    markdownMaker = Markdown()
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/entryNotExist.html", {
            "title": title
        })

    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdownMaker.convert(entry),
            "title": title
        })


# Searching entry
def search(request):
    query = request.GET.get("q")

    list_of_entries = util.list_entries()
    if query in list_of_entries:
        return HttpResponseRedirect(reverse(
            "entry",
            kwargs={"title": query}
        ))
    else:
        list_of_possible_result = [entry for entry in list_of_entries if query.lower() in entry.lower()]

        # for entries in list_of_entries:
        #     if query.lower() in entries.lower():
        #         found = True
        #         list_of_possible_result.append(entries)
        # list_of_possible_result.sort()

        return render(request, "encyclopedia/search.html", {
            "query": query,
            "found": len(list_of_possible_result) != 0,
            "results": list_of_possible_result
        })


# Create new entry and add to the directory
def add_entry(request):

    if request.method == "POST":
        form = forms.AddNewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse(
                "entry",
                kwargs={"title": title}
            ))

        else:
            return render(request, "encyclopedia/addEntry.html", {
                "form": forms.AddNewEntryForm(request.POST)
            })

    else:
        return render(request, "encyclopedia/addEntry.html", {
            "form": forms.AddNewEntryForm(),
        })


# Edit the content of existing entry
def edit_entry(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        form = forms.EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
        
            return HttpResponseRedirect(reverse(
                "entry",
                kwargs={"title": title}
            ))

    else:
        if entry is None:
            return render(request, "encyclopedia/entryNotExist.html", {
                "title": title
            })
            
        else:
            form = forms.EditEntryForm()
            form.fields["content"].initial = entry
            return render(request, "encyclopedia/editEntry.html", {
                "title": title,
                "form": form,
            })


# Go to a random entry
def random_page(request):
    return HttpResponseRedirect(reverse(
        "entry",
        kwargs={"title": random.choice(util.list_entries())}
    ))
