from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Report(models.Model):
  # TODO: add learning material model to allowed_related_model once its implemented
  description = models.TextField()

  allowed_related_models = models.Q(app_label='comment', model='comment')
  content_type = models.ForeignKey(
      ContentType,
      on_delete=models.CASCADE,
      limit_choices_to=allowed_related_models,
      related_name='report_type',
  )
  object_id = models.PositiveIntegerField()
  report_of = GenericForeignKey(
      ct_field='content_type',
      fk_field='object_id',
  )

  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    indexes = [
        models.Index(fields=["content_type", "object_id"])
    ]

  def __str__(self) -> str:
    return f'Report(report_of={self.report_of}, description={self.description})'
