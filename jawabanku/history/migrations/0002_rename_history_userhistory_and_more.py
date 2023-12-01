# Generated by Django 4.2.7 on 2023-12-01 20:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("history", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="History",
            new_name="UserHistory",
        ),
        migrations.RenameIndex(
            model_name="userhistory",
            new_name="history_use_content_96a9e4_idx",
            old_name="history_his_content_774c23_idx",
        ),
    ]
