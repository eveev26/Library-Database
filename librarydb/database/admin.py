from django.contrib import admin

from .models import LibraryBranch, User, Activity, Book

class BookInline(admin.StackedInline):
    model = Book
    extra = 3

class LibraryBranchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["branch_name", "address"]}),
        # ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [BookInline]

admin.site.register(LibraryBranch)
admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Book)