from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from jawabanku.admin import admin_site

from .models import Report


@register(Report, site=admin_site)
class ReportAdmin(ModelAdmin):
  list_display = ['id', 'description', 'report_of']
