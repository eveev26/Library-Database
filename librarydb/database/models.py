import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

# class LibraryBranch(models.Models):
#     pass

class Book(models.Models):
    title = models.CharField(max_length=100)
    author = models.CharField
    pub_date = models.DateField()
    # library = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE)
    # on_loan = models.BooleanField(default=False)

class LibraryBranch(models.Models):
    branch_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    books = {models.ForeignKey(Book, on_delete=models.CASCADE):models.IntegerField}

class User(models.Models):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    fees = models.FloatField(default=0)
    member_since = models.DateTimeField()
    signed_out = models.ForeignKey(Book, on_delete=models.CASCADE, max_length=5)

class Activity(models.Models):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE)
    loan_date = models.DateTimeField()
    return_date = models.DateTimeField(default=loan_date + datetime.timedelta(days=21))