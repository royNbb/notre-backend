from typing import Optional

from account.models import Account
from .models import Category, Material
from django.db import transaction
from django.db.models import QuerySet


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

            print(material)
            if validated_data.get("categories"):
                material.categories.set(validated_data.get("categories"))
            return material
        except Exception as e:
            print(e)
            return None
