# Generated by Django 4.1.4 on 2023-01-03 07:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0003_book_cover_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookreview",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]