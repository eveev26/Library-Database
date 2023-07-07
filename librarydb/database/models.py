import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Book(models.Models):
    title = models.CharField(max_length=100)
    author = models.CharField
    pub_date = models.DateTimeField()

class LibraryBranch(models.Models):
    branch_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)

class User(models.Models):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    fees = models.FloatField(default=0)
    signed_out = models.ForeignKey(Book, on_delete=models.CASCADE)