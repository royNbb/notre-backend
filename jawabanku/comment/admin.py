from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from jawabanku.admin import admin_site

from .models import Comment


@register(Comment, site=admin_site)
class CommentAdmin(ModelAdmin):
  list_display = ['id', 'owner', 'material', 'content']
