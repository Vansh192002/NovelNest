# Generated by Django 5.1.7 on 2025-03-18 09:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_book_collection_genre_readlist_userprofile_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='genre',
            new_name='summary',
        ),
        migrations.RemoveField(
            model_name='readlist',
            name='status',
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(related_name='books', to='home.genre'),
        ),
        migrations.AddField(
            model_name='collection',
            name='status',
            field=models.CharField(blank=True, choices=[('TBR', 'TO READ'), ('Reading', 'Currently Reading'), ('Read', 'Read')], max_length=25),
        ),
        migrations.AddField(
            model_name='readlist',
            name='read',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=300),
        ),
    ]
