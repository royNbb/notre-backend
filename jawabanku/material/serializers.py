from rest_framework import serializers

from account.serializers import AccountSerializer
from .models import Category, Material
from rest_framework.serializers import IntegerField, CharField, ListField, PrimaryKeyRelatedField


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']


class MaterialSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Material
        fields = ['id', 'slug', 'title', 'description', 'content', 'owner', 'categories']


class CreateMaterialSerializer(serializers.ModelSerializer):
    title = CharField(required=True)
    description = CharField(required=True)
    content = CharField(required=True)
    owner_id = IntegerField(required=True)
    categories = PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    
    class Meta:
        model = Material
        fields = ['title', 'description', 'content', 'owner_id', 'categories']
