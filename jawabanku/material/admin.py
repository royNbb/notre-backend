from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from jawabanku.admin import admin_site

from .models import Category
from .models import Material


@register(Category, site=admin_site)
class CategoryAdmin(ModelAdmin):
  list_display = ['id', 'name', 'type']

@register(Material, site=admin_site)
class MaterialAdmin(ModelAdmin):
  list_display = ['id', 'slug', 'title', 'description', 'content', 'owner']
