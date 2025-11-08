from django.shortcuts import render, HttpResponse, redirect
import random
import markdown2
from django.utils.safestring import mark_safe
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return HttpResponse("Requested entry was not found!")
    else:
        html = markdown2.markdown(content)
        Entry = mark_safe(html)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "Entry": Entry
        })
    
def search(request):
    entries = util.list_entries()
    if request.method == "POST":
        encyclopedia_entry = request.POST.get('q')
        if encyclopedia_entry  in entries:
            return redirect('entry', title=encyclopedia_entry)
        else:
            for i in entries[0:]:     
                if encyclopedia_entry in i:
                    return render(request, "encyclopedia/search.html", {
                    "title": encyclopedia_entry,
                    "Entry": i
        })
    return render(request, "encyclopedia/index.html")

def newPage(request):
    entries = util.list_entries()
    if request.method == "POST":
        query = request.POST.get("title")
        content = request.POST.get("content")
        if query in entries:
            return HttpResponse(f"error!!, this title '{query}' already exist")
        else:
            with open(f"entries/{query}.md", 'w') as page:
                page.write(content)
                page.close()
                return redirect('entry', title=query)
    return render(request, "encyclopedia/newpage.html")

def editPage(request, title):
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect( "editPage", title=title)
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": content
    })
    else:
        return HttpResponse("page not found")

def randomPage(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return render(request, "encyclopedia/randompage.html", {
        "Entry": random_entry
    })