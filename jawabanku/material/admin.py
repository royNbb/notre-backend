from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from jawabanku.admin import admin_site

from .models import Category


@register(Category, site=admin_site)
class CategoryAdmin(ModelAdmin):
  list_display = ['id', 'name', 'type']
