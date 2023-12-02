from rest_framework.serializers import CharField
from rest_framework.serializers import EmailField
from rest_framework.serializers import ModelSerializer

from account.serializers import AccountSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
  owner = AccountSerializer(many=False, read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'owner', 'content', 'created_at', 'updated_at']
