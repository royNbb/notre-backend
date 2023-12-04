from rest_framework import serializers

from account.serializers import AccountSerializer
from .models import Category, Material, Tag
from rest_framework.serializers import IntegerField, CharField, PrimaryKeyRelatedField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']


class MaterialSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format="%d %b %Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d %b %Y %H:%M:%S")

    class Meta:
        model = Material
        fields = ['id', 'slug', 'title', 'description', 'content', 'owner', 'categories', 'tags', "created_at", 'updated_at']


class CreateMaterialSerializer(serializers.ModelSerializer):
    title = CharField(required=True)
    description = CharField(required=True)
    content = CharField(required=True)
    owner_id = IntegerField(required=True)
    categories = PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Material
        fields = ['title', 'description', 'content', 'owner_id', 'categories', 'tags']


class UpdateMaterialSerializer(serializers.ModelSerializer):
    title = CharField(required=False)
    description = CharField(required=False)
    content = CharField(required=False)
    categories = PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Material
        fields = ['title', 'description', 'content', 'categories', 'tags']
