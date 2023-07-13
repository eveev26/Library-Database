import datetime

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField



# class LibraryBranch(models.Models):
#     pass

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    pub_date = models.DateField()
    summary = models.CharField(max_length=1000, null=True)
    isbn = models.IntegerField(null=True)
    # copies = models.IntegerField(default=1)
    # library = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE, null=True)
    # library = models.ManyToManyField(LibraryBranch)
    # available = models.IntegerField(default=0)

    # class Meta:
    #     ordering = ["title"]

    def __str__(self):
        return self.title + ' by ' + self.author
    
class LibraryBranch(models.Model):
    branch_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    class Meta:
        ordering = ["branch_name"]

    def __str__(self):
        return self.branch_name
    
class User(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    lib_card = models.BigIntegerField(unique=True, null=True)
    fees = models.FloatField(default=0)
    member_since = models.DateTimeField()
    signed_out = models.ForeignKey(Book, on_delete=models.CASCADE, max_length=5)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE)
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