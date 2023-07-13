# Generated by Django 4.2.3 on 2023-07-13 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_alter_book_options_remove_book_library_book_library'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.AlterModelOptions(
            name='librarybranch',
            options={'ordering': ['branch_name']},
        ),
        migrations.RemoveField(
            model_name='book',
            name='library',
        ),
        migrations.AddField(
            model_name='book',
            name='on_loan',
            field=models.IntegerField(default=models.IntegerField(default=1)),
        ),
        migrations.AddField(
            model_name='librarybranch',
            name='books',
            field=models.ManyToManyField(to='database.book'),
        ),
    ]