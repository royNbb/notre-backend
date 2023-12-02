from typing import Optional

from account.models import Account
from .models import Category, Material, Tag
from django.db import transaction
from django.db.models import QuerySet


class TagAccessors:
    def get_tag_by_id(self, tag_id: int) -> Optional[Tag]:
        try:
            tag = Tag.objects.get(pk=tag_id)
            return tag
        except Tag.DoesNotExist:
            return None


class CategoryAccessors:
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        try:
            category = Category.objects.get(pk=category_id)
            return category
        except Category.DoesNotExist:
            return None


class MaterialAccessors:
    def get_all_materials(self) -> Optional[QuerySet[Material]]:
        try:
            materials = Material.objects.all()
            return materials
        except Material.DoesNotExist:
            return None

    def get_material_by_id(self, material_id: int) -> Optional[Material]:
        try:
            material = Material.objects.get(pk=material_id)
            return material
        except Material.DoesNotExist:
            return None

    def create_material(self, account: Account, **validated_data) -> Optional[Material]:
        try:
            material = Material.objects.create(
                title=validated_data.get("title"),
                description=validated_data.get("description"),
                content=validated_data.get("content"),
                owner=account,
            )
            if validated_data.get("categories"):
                material.categories.set(validated_data.get("categories"))
            if validated_data.get("tags"):
                material.tags.set(validated_data.get("tags"))
            return material
        except Exception as e:
            return None

    def update_material(self, material: Material, **validated_data) -> Optional[Material]:
        try:
            with transaction.atomic():
                for key, value in validated_data.items():
                    if key != 'categories' and key != 'tags':
                        setattr(material, key, value)

                categories = validated_data.get('categories')
                tags = validated_data.get('tags')

                if categories is not None:
                    material.categories.set(categories)

                if tags is not None:
                    material.tags.set(tags)
                else:
                    material.tags.clear()

                material.save()
                return material
        except Exception as e:
            return None

    def delete_material(self, material: Material) -> bool:
        try:
            material.delete()
            return True
        except Exception as e:
            return False
