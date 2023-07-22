from django.contrib import admin

from .models import User, Activity, Book, BooksAvailable, LibraryBranch

class BooksAvailableInline(admin.StackedInline):
    model = BooksAvailable
    extra = 1

class BookAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {"fields": ["available", "copies"]}),
    # ]
    inlines = [BooksAvailableInline]

# class AvailabilityInline(admin.TabularInline):
#     model = LibraryBranch.books.through


# class BooksAvailableAdmin(admin.ModelAdmin):
#     inlines = [
#         AvailabilityInline,
#     ]


# class LibraryBranchAdmin(admin.ModelAdmin):
#     inlines = [
#         AvailabilityInline,
#     ]
#     exclude = ["books"]

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Book, BookAdmin)
admin.site.register(BooksAvailable)
# admin.site.register(LibraryBranch, LibraryBranchAdmin)
admin.site.register(LibraryBranch)