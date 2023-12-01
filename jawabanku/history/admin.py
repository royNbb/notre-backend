from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from jawabanku.admin import admin_site

from .models import History


@register(History, site=admin_site)
class HistoryAdmin(ModelAdmin):
  list_display = ['id', 'owner', 'history_of']
