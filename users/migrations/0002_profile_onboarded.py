# Generated by Django 4.2 on 2024-02-18 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="onboarded",
            field=models.BooleanField(default=False),
        ),
    ]
