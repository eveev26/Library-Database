from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from .models import Book, LibraryBranch, BooksAvailable
from django.template import loader

def index(request):
    book_list = Book.objects.order_by("-title")
    library_list = LibraryBranch.objects.order_by("-branch_name")
    availability_list = BooksAvailable.objects.order_by("-id")
    template = loader.get_template("database/index.html")
    context = {
        "book_list": book_list,
        "library_list": library_list,
        "availability_list": availability_list,
    }
    return HttpResponse(template.render(context, request))
    
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    avail = []
    for i in BooksAvailable.objects.all():
        if i.book_id == book.id:
            avail.append(i)
    
    libraries = []
    for j in LibraryBranch.objects.all():
        for k in j.books.all():
            if k in avail:
                libraries.append(j.branch_name)
    
    return render(request, "database/detail.html", {"book": book, "libraries": libraries})

# def detail(request, book_id):
#     try:
#         book = Book.objects.get(pk=book_id)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
#     return render(request, "database/detail.html", {"book": book})