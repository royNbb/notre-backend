from ctypes import FormatError
from rest_framework.serializers import CharField
from rest_framework.serializers import EmailField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import SerializerMethodField

from account.serializers import AccountSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    owner = AccountSerializer(many=False, read_only=True)
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S")  # type: ignore
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S")  # type: ignore

    class Meta:
        model = Comment
        fields = ["id", "owner", "content", "created_at", "updated_at"]
