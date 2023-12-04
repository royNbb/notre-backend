from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from account.models import Account


class UserHistory(models.Model):
  owner = models.ForeignKey(Account, on_delete=models.CASCADE)

  allowed_related_models = models.Q(app_label='comment', model='comment') | models.Q(app_label='report', model='report') | models.Q(app_label='material', model='material')
  content_type = models.ForeignKey(
      ContentType,
      on_delete=models.CASCADE,
      limit_choices_to=allowed_related_models,
      related_name='history_type'
  )
  object_id = models.PositiveIntegerField()
  history_of = GenericForeignKey(
      ct_field='content_type',
      fk_field='object_id',
  )

  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    indexes = [
        models.Index(fields=["content_type", "object_id"]),
    ]

  def __str__(self) -> str:
    return f'UserHistory(owner={self.owner}, type={self.history_of})'
