from rest_framework.serializers import CharField
from rest_framework.serializers import EmailField
from rest_framework.serializers import ModelSerializer, Field

from rest_framework.serializers import IntegerField, CharField, PrimaryKeyRelatedField

from material.models import Material
from account.models import Account
from .models import Comment

from account.serializers import AccountSerializer
from material.serializers import MaterialSerializer


class EpochDateTimeField(Field):
  def to_representation(self, value):
    return value.timestamp() if value else None


class CommentSerializer(ModelSerializer):
  owner = AccountSerializer(many=False, read_only=True)
  material = MaterialSerializer(many=False, read_only=True)

  created_at = EpochDateTimeField()
  updated_at = EpochDateTimeField()

  class Meta:
    model = Comment
    fields = ['id', 'owner', 'material', 'content', 'created_at', 'updated_at']


class CreateCommentSerializer(ModelSerializer):
  material = PrimaryKeyRelatedField(queryset=Material.objects.all())
  content = CharField(required=True)
  owner_id = IntegerField(required=True)

  class Meta:
    model = Comment
    fields = ['material', 'content', 'owner_id']


class UpdateCommentSerializer(ModelSerializer):
  content = CharField(required=True)

  class Meta:
    model = Comment
    fields = ['content']
