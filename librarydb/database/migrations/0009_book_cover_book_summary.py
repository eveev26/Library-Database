# Generated by Django 4.2.3 on 2023-07-11 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_remove_book_cover_remove_book_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
