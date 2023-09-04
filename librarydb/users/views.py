from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from database.models import User, Activity, BooksAvailable;
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseRedirect

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/database/')
        else:
            messages.success(request, ("There Was An Error Logging In. Try Again"))
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out"))
    return redirect('http://127.0.0.1:8000/database/')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            User.objects.create(username=username)
            login(request, user)
            messages.success(request, ("Registration Successful"))
            return redirect('http://127.0.0.1:8000/database/')
    else:
        form = UserCreationForm()

    context = {'form': form,}
    return render(request, 'authentication/register_user.html', context)

def account(request):
        
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/users/login_user')
    else:
        username = get_object_or_404(User, username=request.user.username)
        print(username)
        # on_loan = Activity.objects.raw('''SELECT *
        #                             FROM database_activity
        #                             WHERE username_id = %s AND return_date >= %s
        #                             ORDER BY return_date;''', username, [models.DateTimeField(auto_now=True)])
        print(username.id)
        on_loan = Activity.objects.raw('''SELECT *
                                    FROM database_activity
                                    WHERE username_id = %s AND return_date >= %s
                                    ORDER BY return_date;''', [username.id, timezone.now()])
        # for i in range(len(on_loan)):
        #     print(on_loan[i])

        if request.method == 'POST':
            try:
                return_book =  request.POST.get("return_book", None)
            except MultiValueDictKeyError:
                return_book = False
            record = Activity.objects.get(pk=return_book)
            record.return_date = timezone.now()
            record.save()
            print("yay", return_book)

            lib = record.library
            # print(lib.books)
            lib = BooksAvailable.objects.raw('''SELECT a.id, a.available, a.book_id, a.copies
                                             FROM database_booksavailable AS a
                                             INNER JOIN database_librarybranch_books AS l
                                                ON l.booksavailable_id = a.id
                                             WHERE l.librarybranch_id = %s AND a.book_id = %s;''', [lib.id, record.book.id])
            # i = BooksAvailable.objects.get()
            # for i in range(len(lib)):
            #     print(lib[i])
            print(lib[0])
                # if book.book == record.book:
            book_available = BooksAvailable.objects.get(pk=lib[0].id)
            book_available.available += 1
            book_available.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        context = {'on_loan': on_loan,
                   'now': timezone.now()}
        return render(request, 'authentication/account.html', context)