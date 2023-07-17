from django.contrib import admin

from .models import User, Activity, Book, BooksAvailable, LibraryBranch

class BookInline(admin.StackedInline):
    model = Book
    extra = 3

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Book)
admin.site.register(BooksAvailable)
admin.site.register(LibraryBranch)