# Generated by Django 4.2.7 on 2023-12-04 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("history", "0002_rename_history_userhistory_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userhistory",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    models.Q(("app_label", "comment"), ("model", "comment")),
                    models.Q(("app_label", "report"), ("model", "report")),
                    models.Q(("app_label", "material"), ("model", "material")),
                    _connector="OR",
                ),
                on_delete=django.db.models.deletion.CASCADE,
                related_name="history_type",
                to="contenttypes.contenttype",
            ),
        ),
    ]
