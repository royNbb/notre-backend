# Generated by Django 4.2.7 on 2023-11-28 08:45

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=128),
            preserve_default=False,
        ),
    ]
