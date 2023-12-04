from django.db import models
from django.utils import timezone

from account.models import Account
from material.models import Material

class Comment(models.Model):
  owner = models.ForeignKey(Account, on_delete=models.CASCADE)
  material = models.ForeignKey(Material, on_delete=models.CASCADE)
  
  content = models.TextField()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return f'Comment(owner={self.owner}, content={self.content})'
