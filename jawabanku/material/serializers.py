from rest_framework import serializers

from account.serializers import AccountSerializer
from .models import Category, Material, Tag
from rest_framework.serializers import IntegerField, CharField, PrimaryKeyRelatedField


class EpochDateTimeField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp() if value else None


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
    created_at = EpochDateTimeField()
    updated_at = EpochDateTimeField()
    
    class Meta:
        model = Material
        fields = ['id', 'slug', 'title', 'description', 'content', 'owner', 'categories', 'tags', 'created_at', 'updated_at']

class CreateCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=256)
    type = serializers.ChoiceField(choices=Category.CategoryType.choices, required=True)
    major = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(type=Category.CategoryType.MAJOR), required=False)

    class Meta:
        model = Category
        fields = ['name', 'type', 'major']

    def validate(self, data):
        if data.get('type') == Category.CategoryType.COURSE and not data.get('major'):
            raise serializers.ValidationError('Course type categories must have a major.')
        return data

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
