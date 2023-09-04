# Generated by Django 4.2.3 on 2023-09-03 03:48

import database.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_date', models.DateTimeField(auto_now=True)),
                ('return_date', models.DateTimeField(default=database.models.Activity.loan_date_time)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.book')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('signed_out', models.ManyToManyField(max_length=5, to='database.activity')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user'),
        ),
    ]