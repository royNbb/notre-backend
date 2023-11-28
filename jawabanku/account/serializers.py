from rest_framework.serializers import CharField
from rest_framework.serializers import EmailField
from rest_framework.serializers import ModelSerializer

from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password', 'created_at', 'updated_at', 'groups', 'user_permissions', 'last_login']


class AccountUpdateSerializer(ModelSerializer):
    name = CharField(required=False)
    username = CharField(required=False)
    email = EmailField(required=False)

    class Meta:
        model = Account
        fields = ['name', 'username', 'email']
