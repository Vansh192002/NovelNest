# Generated by Django 5.1.7 on 2025-03-25 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_book_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='ebooks/thumbnails/'),
        ),
    ]
