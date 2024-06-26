# Generated by Django 4.2.7 on 2023-12-03 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('report', '0003_report_reporter_report_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(('app_label', 'comment'), ('model', 'comment')), on_delete=django.db.models.deletion.CASCADE, related_name='report_type', to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
