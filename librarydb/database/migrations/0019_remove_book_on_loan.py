# Generated by Django 4.2.3 on 2023-07-13 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_book_on_loan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='on_loan',
        ),
    ]