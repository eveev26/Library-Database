from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Book, LibraryBranch, BooksAvailable, Activity, User
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError

from django.core.paginator import Paginator

def index(request):
    book_list = Book.objects.raw('''SELECT b.id, b.title, b.author, b.pub_date, b.summary, b.isbn 
                                 FROM database_librarybranch AS l 
                                 INNER JOIN database_librarybranch_books AS lb 
                                    ON l.id = lb.librarybranch_id 
                                 INNER JOIN database_booksavailable AS a 
                                    ON a.id = lb.booksavailable_id 
                                 INNER JOIN database_book as b 
                                    ON b.id = a.book_id 
                                 ORDER BY b.title;''')
    
    library_list = LibraryBranch.objects.raw('''SELECT l.id, l.branch_name, l.address 
                                             FROM database_librarybranch AS l 
                                             INNER JOIN database_librarybranch_books AS lb 
                                                ON l.id = lb.librarybranch_id 
                                             INNER JOIN database_booksavailable AS a 
                                                ON a.id = lb.booksavailable_id 
                                             INNER JOIN database_book as b 
                                                ON b.id = a.book_id 
                                             ORDER BY b.title;''')

    if request.method == 'POST':
        try:
            field =  request.POST.get("field", None)
        except MultiValueDictKeyError:
            field = False

        print(field)
        if field == 'author':
            book_list = Book.objects.raw('''SELECT b.id, b.title, b.author, b.pub_date, b.summary, b.isbn 
                                         FROM database_librarybranch AS l 
                                         INNER JOIN database_librarybranch_books AS lb 
                                            ON l.id = lb.librarybranch_id 
                                         INNER JOIN database_booksavailable AS a 
                                            ON a.id = lb.booksavailable_id 
                                         INNER JOIN database_book as b 
                                            ON b.id = a.book_id 
                                         ORDER BY b.author;''')
            
            library_list = LibraryBranch.objects.raw('''SELECT l.id, l.branch_name, l.address 
                                                     FROM database_librarybranch AS l 
                                                     INNER JOIN database_librarybranch_books AS lb 
                                                        ON l.id = lb.librarybranch_id 
                                                     INNER JOIN database_booksavailable AS a 
                                                        ON a.id = lb.booksavailable_id 
                                                     INNER JOIN database_book as b 
                                                        ON b.id = a.book_id 
                                                     ORDER BY b.author;''')
            
        in_list = False
        book_library_list = [] #[[book1, [lib1, lib2]], ]
        for i in range(len(book_list)):
            in_list = False
            print(book_library_list, '\n\n')
            for j in range(len(book_library_list)):
                if book_library_list[j][0] == book_list[i]:
                    book_library_list[j][1].append(library_list[i])
                    in_list = True
            if not in_list:
                book_library_list.append([book_list[i], [library_list[i]]])
        
        p = Paginator(book_library_list, 10)
        page = request.GET.get('page')
        books = p.get_page(page)


        context = {
            "book_list": book_list,
            "library_list": library_list,
            "book_library_list": book_library_list,
            "books": books,
        }

        return render(request, 'database/index.html', context)
    else:

        in_list = False
        book_library_list = [] #[[book1, [lib1, lib2]], ]
        for i in range(len(book_list)):
            in_list = False
            for j in range(len(book_library_list)):
                if book_library_list[j][0] == book_list[i]:
                    book_library_list[j][1].append(library_list[i])
                    in_list = True
            if not in_list:
                book_library_list.append([book_list[i], [library_list[i]]])

        p = Paginator(book_library_list, 10)
        page = request.GET.get('page')
        books = p.get_page(page)

        context = {
            "book_list": book_list,
            "library_list": library_list,
            "book_library_list": book_library_list,
            "books": books,
        }
        return render(request, 'database/index.html', context)
    
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    libraries = LibraryBranch.objects.raw('''SELECT l.id, l.branch_name, l.address 
                                          FROM database_librarybranch AS l 
                                          INNER JOIN database_librarybranch_books AS lb 
                                            ON l.id = lb.librarybranch_id 
                                          INNER JOIN database_booksavailable AS a 
                                            ON a.id = lb.booksavailable_id 
                                          INNER JOIN database_book as b 
                                            ON b.id = a.book_id 
                                          WHERE b.id = %s 
                                          ORDER BY b.title ;''', [book.id])
    
    availability = BooksAvailable.objects.raw('''SELECT a.id, a.available, a.book_id, a.copies 
                                          FROM database_librarybranch AS l 
                                          INNER JOIN database_librarybranch_books AS lb 
                                            ON l.id = lb.librarybranch_id 
                                          INNER JOIN database_booksavailable AS a 
                                            ON a.id = lb.booksavailable_id 
                                          INNER JOIN database_book as b 
                                            ON b.id = a.book_id 
                                          WHERE b.id = %s 
                                          ORDER BY b.title ;''', [book.id])
    
    availability_list = {}
    for i in range(len(libraries)):
        availability_list[libraries[i]] = [availability[i].available, availability[i].copies]

    if request.method == 'POST':
        try:
            borrow =  request.POST.get("borrow", None)
        except MultiValueDictKeyError:
            borrow = False
        
        print(borrow)
        # Activity.objects.create()
        if not request.user.is_authenticated:
            return redirect('/users/login_user')
        else:
            # lib_user = User.objects.raw('''SELECT *
            #                     FROM database_user
            #                     WHERE username = %s;''', [request.user.username])
            lib_user = get_object_or_404(User, username=request.user.username)
            print("happy", lib_user)
            Activity.objects.create(username=lib_user, book=book, library=LibraryBranch.objects.get(branch_name=borrow))
            idx = 0
            for i in range(len(libraries)):
                if libraries[i] == LibraryBranch.objects.get(branch_name=borrow):
                    idx = i
            record = BooksAvailable.objects.get(pk=availability[idx].id)
            record.available -= 1
            record.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    print(availability_list)
    
    context = {"book": book,
               "availability_list": availability_list}
    
    return render(request, "database/detail.html", context)

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