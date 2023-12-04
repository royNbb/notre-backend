# Generated by Django 4.2.7 on 2023-12-02 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'comment'), ('model', 'comment')), models.Q(('app_label', 'material'), ('model', 'material')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='report_type', to='contenttypes.contenttype'),
        ),
    ]
