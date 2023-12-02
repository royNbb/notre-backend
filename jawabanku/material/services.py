from typing import Optional

from account.models import Account
from material.serializers import CreateMaterialSerializer, UpdateMaterialSerializer
from .models import Category, Material, Tag
from .accessors import CategoryAccessors, MaterialAccessors, TagAccessors
from django.db.models import QuerySet


class TagServices:
    tag_accessors = TagAccessors()

    def get_tag_by_id(self, tag_id: int) -> Optional[Tag]:
        return self.tag_accessors.get_tag_by_id(tag_id)


class CategoryServices:
    category_accessors = CategoryAccessors()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_accessors.get_category_by_id(category_id)


class MaterialServices:
    material_accessors = MaterialAccessors()

    def get_all_materials(self) -> Optional[QuerySet[Material]]:
        return self.material_accessors.get_all_materials()

    def get_material_by_id(self, material_id: int) -> Optional[Material]:
        return self.material_accessors.get_material_by_id(material_id)

    def create_material(self, account: Account, **kwargs) -> Optional[Material]:
        parsed_data = {}
        parsed_data['owner_id'] = account.id
        if kwargs.get('title', None):
            parsed_data['title'] = kwargs.get('title')
        if kwargs.get('description', None):
            parsed_data['description'] = kwargs.get('description')
        if kwargs.get('content', None):
            parsed_data['content'] = kwargs.get('content')
        if kwargs.get('categories', []):
            parsed_data['categories'] = kwargs.get('categories')
        if kwargs.get('tags', []):
            parsed_data['tags'] = kwargs.get('tags')

        serialized_req = CreateMaterialSerializer(data=parsed_data, many=False)
        if serialized_req.is_valid():
            data = serialized_req.validated_data
            return self.material_accessors.create_material(account, **data)

        return None

    def update_material(self, material: Material, **kwargs) -> Optional[Material]:
        parsed_data = {}
        if kwargs.get('title', None):
            parsed_data['title'] = kwargs.get('title')
        if kwargs.get('description', None):
            parsed_data['description'] = kwargs.get('description')
        if kwargs.get('content', None):
            parsed_data['content'] = kwargs.get('content')
        if kwargs.get('categories', []):
            parsed_data['categories'] = kwargs.get('categories')
        if kwargs.get('tags', []):
            parsed_data['tags'] = kwargs.get('tags')

        serialized_req = UpdateMaterialSerializer(data=parsed_data, many=False)
        if serialized_req.is_valid():
            data = serialized_req.validated_data
            return self.material_accessors.update_material(material, **data)

        return None

    def delete_material(self, material: Material) -> None:
        return self.material_accessors.delete_material(material)
