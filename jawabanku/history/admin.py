from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from jawabanku.admin import admin_site

from .models import UserHistory


@register(UserHistory, site=admin_site)
class UserHistoryAdmin(ModelAdmin):
  list_display = ['id', 'owner', 'history_of']
