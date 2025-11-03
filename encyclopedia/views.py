from django.shortcuts import render, HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    Entry = util.get_entry(title)
    if Entry is None:
        return HttpResponse("Requested entry was not found!")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "Entry": Entry
        })
