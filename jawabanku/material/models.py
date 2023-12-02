from django.db import models
from django.utils import timezone


class Category(models.Model):
  class CategoryType(models.TextChoices):
    SUBJECT = 'Subject', 'subject'
    TOPIC = 'Topic', 'topic'
  name = models.CharField(max_length=256, unique=True)
  type = models.CharField(max_length=16, choices=CategoryType.choices)

  created_at = models.DateTimeField(default=timezone.now)
  update_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return f'Category(name={self.name}, type={self.type})'
