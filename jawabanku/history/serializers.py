from rest_framework.serializers import IntegerField, CharField
from rest_framework.serializers import EmailField
from rest_framework.serializers import ModelSerializer, SerializerMethodField, RelatedField

from .models import UserHistory

from comment.models import Comment
from comment.serializers import CommentSerializer

from report.models import Report
from report.serializers import ReportSerializer


class HistoryRelatedField(RelatedField):
  def to_representation(self, value):
    if isinstance(value, Comment):
      serializer = CommentSerializer(value, many=False)
    elif isinstance(value, Report):
      serializer = ReportSerializer(value, many=False)
    else:
      raise Exception("Unexpected type of history related model")
    return serializer.data


class UserHistorySerializer(ModelSerializer):
  history_type = SerializerMethodField("get_history_type")
  history_of = HistoryRelatedField(read_only=True)

  def get_history_type(self, user_history: UserHistory):
    return user_history.content_type.model

  class Meta:
    model = UserHistory
    fields = ['id', 'owner', 'history_of', 'history_type', 'created_at']


class CreateUserHistorySerializer(ModelSerializer):
  owner_id = IntegerField(required=True)
  related_model_name = CharField(required=True)
  related_model_app_label = CharField(required=True)
  related_model_id = IntegerField(required=True)

  class Meta:
    model = UserHistory
    fields = ['owner_id', 'related_model_name', 'related_model_app_label', 'related_model_id']
