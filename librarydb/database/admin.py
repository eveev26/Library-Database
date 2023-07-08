from django.contrib import admin

from .models import LibraryBranch, User, Activity, Book

admin.site.register(LibraryBranch)
admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Book)