from rest_framework.serializers import CharField
from rest_framework.serializers import EmailField
from rest_framework.serializers import ModelSerializer

from rest_framework.serializers import IntegerField, CharField, PrimaryKeyRelatedField

from material.models import Material
from account.models import Account
from .models import Comment

from account.serializers import AccountSerializer
from material.serializers import MaterialSerializer



class CommentSerializer(ModelSerializer):
  owner = AccountSerializer(many=False, read_only=True)
  material = MaterialSerializer(many=False, read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'owner', 'material', 'content', 'created_at', 'updated_at']

class CreateCommentSerializer(ModelSerializer):
    content = CharField(required=True)
    owner = PrimaryKeyRelatedField(queryset=Account.objects.all())
    material = PrimaryKeyRelatedField(queryset=Material.objects.all())

    class Meta:
        model = Comment
        fields = ['owner', 'material', 'content']

class UpdateCommentSerializer(ModelSerializer):
    content = CharField(required=True)

    class Meta:
        model = Comment
        fields = ['content']
