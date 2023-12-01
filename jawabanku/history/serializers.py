from rest_framework.serializers import IntegerField, CharField
from rest_framework.serializers import EmailField
from rest_framework.serializers import ModelSerializer

from .models import UserHistory


class UserHistorySerializer(ModelSerializer):
  class Meta:
    model = UserHistory


class CreateUserHistorySerializer(ModelSerializer):
  owner_id = IntegerField(required=True)
  related_model_name = CharField(required=True)
  related_model_app_label = CharField(required=True)
  related_model_id = IntegerField(required=True)

  class Meta:
    model = UserHistory
    fields = ['owner_id', 'related_model_name', 'related_model_app_label', 'related_model_id']
