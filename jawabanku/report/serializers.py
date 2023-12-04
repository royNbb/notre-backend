from rest_framework.serializers import (
    ModelSerializer,
    RelatedField,
    SerializerMethodField,
    DateTimeField,
)
from django.db.models import QuerySet
from .models import Report

from comment.models import Comment
from comment.serializers import CommentSerializer

from material.models import Material
from material.serializers import MaterialSerializer


class ReportRelatedField(RelatedField):
  def to_representation(self, value):
    if isinstance(value, Comment):
      serializer = CommentSerializer(value, many=False)
    elif isinstance(value, Material):
      serializer = MaterialSerializer(value, many=False)
    else:
      raise Exception("Unexpected type of report related model")
    return serializer.data


class ReportSerializer(ModelSerializer):
  report_of = ReportRelatedField(read_only=True)
  report_type = SerializerMethodField("get_report_type")
  created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S")  # type: ignore

  def get_report_type(self, report: Report):
    return report.content_type.model

  class Meta:
    model = Report
    fields = ["id", "description", "report_type", "report_of", "created_at"]
