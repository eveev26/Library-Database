import datetime

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    pub_date = models.DateField()
    summary = models.CharField(max_length=9000, null=True)
    isbn = models.CharField(max_length=14, null=True, blank=True)
    # copies = models.IntegerField(default=1)
    # available = models.IntegerField(default=0)

    # class Meta:
    #     ordering = ["title"]

    def __str__(self):
        return self.title + ' by ' + self.author
    
class BooksAvailable(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    available = models.IntegerField(default=0)
    copies = models.IntegerField(default=0)

    def __str__(self):
        return self.book.title + ", " + str(self.id)
    
class LibraryBranch(models.Model):
    branch_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    books = models.ManyToManyField(BooksAvailable)

    class Meta:
        ordering = ["branch_name"]

    def __str__(self):
        return self.branch_name

class Activity(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE, null=True)
    loan_date = models.DateTimeField(auto_now=True)
    def loan_date_time():
        now = timezone.now()
        return now + datetime.timedelta(days=21)
    return_date = models.DateTimeField(default=loan_date_time)

    # def clean(self):
    #     if not self.return_date:
    #         self.return_date = self.loan_date + datetime.timedelta(days=21)

    # def save(self, **kwargs):
    #     self.clean()
    #     return super().save(**kwargs)

    def __str__(self):
        return self.username.username
        # return self.username.username + ", " + self.book.title + ", " + self.loan_date + " - " + self.return_date

class User(models.Model):
    username = models.CharField(max_length=50)
    # address = models.CharField(max_length=100)
    # lib_card = models.BigIntegerField(unique=True, null=True)
    # fees = models.FloatField(default=0)
    # member_since = models.DateTimeField()
    signed_out = models.ManyToManyField(Activity, max_length=5, blank=True)

    def __str__(self):
        return self.username;