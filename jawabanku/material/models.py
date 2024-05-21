from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from account.models import Account


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Tag(name={self.name})'


class Category(models.Model):
    class CategoryType(models.TextChoices):
        MAJOR = 'Major', 'major'
        CLASS = 'Class', 'class'
    name = models.CharField(max_length=256, unique=True)
    type = models.CharField(max_length=16, choices=CategoryType.choices)

    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Category(name={self.name}, type={self.type})'

#TODO: temporary blank
class Material(models.Model):
    slug = models.SlugField(max_length=255, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(f'{self.title} {self.id}')

    def __str__(self):
        return self.title
