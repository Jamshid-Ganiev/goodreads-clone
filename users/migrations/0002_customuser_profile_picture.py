# Generated by Django 4.1.4 on 2023-01-02 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="profile_picture",
            field=models.ImageField(default="default_profile_img.jpg", upload_to=""),
        ),
    ]