from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from .models import Book, LibraryBranch
from django.template import loader

def index(request):
    book_list = Book.objects.order_by("-title")
    library_list = LibraryBranch.objects.order_by("-branch_name")
    template = loader.get_template("database/index.html")
    context = {
        "book_list": book_list,
        "library_list": library_list,
    }
    return HttpResponse(template.render(context, request))
    
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    library_list = LibraryBranch.objects.all()
    return render(request, "database/detail.html", {"book": book, "library_list": library_list})

# def detail(request, book_id):
#     try:
#         book = Book.objects.get(pk=book_id)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
#     return render(request, "database/detail.html", {"book": book})