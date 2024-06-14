from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from account.models import Account
from django.core.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Tag(name={self.name})'

#TODO: tambah dependency kalo category type nya class, harus ada majornya
class Category(models.Model):
    class CategoryType(models.TextChoices):
        MAJOR = 'Major', 'major'
        COURSE = 'Course', 'course'
    
    name = models.CharField(max_length=256, unique=True)
    type = models.CharField(max_length=16, choices=CategoryType.choices)
    major = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        limit_choices_to={'type': 'Major'}
    )

    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Category(name={self.name}, type={self.type})'

    def clean(self):
        if self.type == self.CategoryType.COURSE and not self.major:
            raise ValidationError('Course type categories must have a major.')

    def save(self, *args, **kwargs):
        self.clean()  # Call clean method to ensure validation
        super().save(*args, **kwargs)  # Call the "real" save() method
        
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
