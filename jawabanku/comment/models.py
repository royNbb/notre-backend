from django.db import models
from django.utils import timezone

from account.models import Account


class Comment(models.Model):
  owner = models.ForeignKey(Account, on_delete=models.CASCADE)
  content = models.TextField()

  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return f'Comment(owner={self.owner}, content={self.content})'
