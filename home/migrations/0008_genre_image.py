# Generated by Django 5.1.7 on 2025-03-21 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_genre_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='image',
            field=models.ImageField(default=1, upload_to='genre-thumbnails/'),
            preserve_default=False,
        ),
    ]
