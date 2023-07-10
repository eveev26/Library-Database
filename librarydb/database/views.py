from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, LibraryBranch
from django.template import loader

def index(request):
    book_list = Book.objects.order_by("-title")
    template = loader.get_template("database/index.html")
    context = {
        "book_list": book_list,
    }
    return HttpResponse(template.render(context, request))
    # output = ", ".join([b.title for b in book_list])
    # return HttpResponse(output)
    