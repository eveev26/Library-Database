from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from .models import Book, LibraryBranch, BooksAvailable
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError

def index(request):
    book_list = Book.objects.order_by("-title")
    library_list = LibraryBranch.objects.order_by("-branch_name")
    availability_list = BooksAvailable.objects.order_by("-id")
    # book_list = LibraryBranch.objects.raw('SELECT l.id, l.branch_name, l.address FROM database_librarybranch AS l INNER JOIN database_librarybranch_books AS lb ON l.id = lb.librarybranch_id INNER JOIN database_booksavailable AS a ON a.id = lb.booksavailable_id INNER JOIN database_book as b on b.id = a.book_id ORDER BY b.title;')
    # library_list = LibraryBranch.objects.raw('SELECT l.id, l.branch_name, l.address FROM database_librarybranch AS l INNER JOIN database_librarybranch_books AS lb ON l.id = lb.librarybranch_id INNER JOIN database_booksavailable AS a ON a.id = lb.booksavailable_id INNER JOIN database_book as b on b.id = a.book_id ORDER BY b.title;')

    if request.method == 'POST':
        try:
            field =  request.POST.get("field", None)
        except MultiValueDictKeyError:
            field = False

        # print(field)

        if field == 'title':
            book_list = Book.objects.raw('SELECT * FROM database_book ORDER BY title;')
            # book_list = LibraryBranch.objects.raw('SELECT l.id, l.branch_name, l.address FROM database_librarybranch AS l INNER JOIN database_librarybranch_books AS lb ON l.id = lb.librarybranch_id INNER JOIN database_booksavailable AS a ON a.id = lb.booksavailable_id INNER JOIN database_book as b on b.id = a.book_id ORDER BY b.title;')
            # library_list = LibraryBranch.objects.raw('SELECT l.id, l.branch_name, l.address FROM database_librarybranch AS l INNER JOIN database_librarybranch_books AS lb ON l.id = lb.librarybranch_id INNER JOIN database_booksavailable AS a ON a.id = lb.booksavailable_id INNER JOIN database_book as b on b.id = a.book_id ORDER BY b.title;')

        elif field == 'author':
            book_list = Book.objects.raw('SELECT * FROM database_book ORDER BY author;')
            # book_list = LibraryBranch.objects.raw('SELECT l.id, l.branch_name, l.address FROM database_librarybranch AS l INNER JOIN database_librarybranch_books AS lb ON l.id = lb.librarybranch_id INNER JOIN database_booksavailable AS a ON a.id = lb.booksavailable_id INNER JOIN database_book as b on b.id = a.book_id ORDER BY b.author;')
            # library_list = LibraryBranch.objects.raw('SELECT l.id, l.branch_name, l.address FROM database_librarybranch AS l INNER JOIN database_librarybranch_books AS lb ON l.id = lb.librarybranch_id INNER JOIN database_booksavailable AS a ON a.id = lb.booksavailable_id INNER JOIN database_book as b on b.id = a.book_id ORDER BY b.author;')
    
        # print(book_list)
        
        context = {
            "book_list": book_list,
            "library_list": library_list,
            "availability_list": availability_list,
            "field": field
        }

        return render(request, 'database/index.html', context)
    else:
        context = {
            "book_list": book_list,
            "library_list": library_list,
            "availability_list": availability_list,
        }
        return render(request, 'database/index.html', context)
    
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

def search(request):
    if request.method == 'POST':
        try:
            searched = request.POST['searched']
        except MultiValueDictKeyError:
            searched = False
        search_result = Book.objects.filter(title__contains=searched)
        library_list = LibraryBranch.objects.order_by("-branch_name")
        availability_list = BooksAvailable.objects.order_by("-id")

        context = {'searched': searched, 
                   'search_result': search_result,
                   "library_list": library_list,
                   "availability_list": availability_list,}
        
        return render(request, 'database/search.html', context)
    else:
        return render(request, 'database/search.html', {})