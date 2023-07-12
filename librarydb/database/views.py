from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from .models import Book, LibraryBranch
from django.template import loader

def index(request):
    book_list = Book.objects.order_by("-title")
    template = loader.get_template("database/index.html")
    context = {
        "book_list": book_list,
    }
    return HttpResponse(template.render(context, request))
    
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "database/detail.html", {"book": book})

# def detail(request, book_id):
#     try:
#         book = Book.objects.get(pk=book_id)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
#     return render(request, "database/detail.html", {"book": book})