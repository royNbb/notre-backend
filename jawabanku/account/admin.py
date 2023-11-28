from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from jawabanku.admin import admin_site

from .models import Account


@register(Account, site=admin_site)
class AccountAdmin(ModelAdmin):
    list_display = ['id', 'email', 'username', 'role', 'is_active']
    exclude = ['password', 'groups']
