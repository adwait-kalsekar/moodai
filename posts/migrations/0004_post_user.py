# Generated by Django 4.2 on 2024-02-18 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile_onboarded"),
        ("posts", "0003_alter_post_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
    ]