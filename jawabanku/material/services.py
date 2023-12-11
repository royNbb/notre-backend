from typing import Optional

from account.models import Account
from material.serializers import CreateMaterialSerializer, UpdateMaterialSerializer
from history.services import HistoryService
from .models import Category, Material, Tag
from .accessors import CategoryAccessors, MaterialAccessors, TagAccessors
from django.db.models import QuerySet

import uuid
from django.core.exceptions import ValidationError
from mimetypes import guess_type

import os
import uuid
import boto3

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'ipynb', 'py', 'java', 'jav', 'c', 'cpp', 'cs', 'go', 'js', 'ts', 'jsx', 'tsx', 'html', 'css', 'php', 'sql', 'swift', 'rb', 'json', 'xml', }
MAX_FILE_SIZE_MB = 20

s3 = boto3.client('s3',
                  region_name=os.getenv('DO_REGION_NAME'),
                  endpoint_url=os.getenv('DO_ENDPOINT_URL'),
                  aws_access_key_id=os.getenv('DO_SPACES_KEY'),
                  aws_secret_access_key=os.getenv('DO_SPACES_SECRET'))


class FileUploadService:
    def upload_file(file_obj, bucket_name):
        try:
            random_hex = uuid.uuid4().hex

            file_extension = file_obj.name.split('.')[-1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                raise ValidationError("Invalid file extension.")

            max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
            if file_obj.size > max_size_bytes:
                raise ValidationError("File size exceeds the maximum allowed.")

            object_name = f'{random_hex}-{file_obj.name}'

            content_type, _ = guess_type(file_obj.name)
            content_type = content_type or 'application/octet-stream'

            s3.upload_fileobj(
                file_obj,
                bucket_name,
                object_name,
                ExtraArgs={'ACL': 'public-read', 'ContentType': content_type}
            )

            file_url = f"https://{bucket_name}.{s3.meta.region_name}.digitaloceanspaces.com/{object_name}"

            return {
                "file_url": file_url,
                "content_type": content_type
            }
        except ValidationError as ve:
            raise ve
        except Exception as e:
            raise e


class TagServices:
    tag_accessors = TagAccessors()

    def get_tag_by_id(self, tag_id: int) -> Optional[Tag]:
        return self.tag_accessors.get_tag_by_id(tag_id)

    def get_all_tags(self) -> Optional[QuerySet[Tag]]:
        return self.tag_accessors.get_all_tags()

    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        return self.tag_accessors.get_tag_by_name(name)


class CategoryServices:
    category_accessors = CategoryAccessors()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_accessors.get_category_by_id(category_id)

    def get_all_categories(self) -> Optional[QuerySet[Category]]:
        return self.category_accessors.get_all_categories()

    def get_category_by_name(self, name: str) -> Optional[Category]:
        return self.category_accessors.get_category_by_name(name)


class MaterialServices:
    material_accessors = MaterialAccessors()

    def get_material_by_id(self, account, material_id: int) -> Optional[Material]:
        material = self.material_accessors.get_material_by_id(material_id)
        HistoryService().create_history(account, **{
            "related_model_app_label": "material",
            "related_model_name": "material",
            "related_model_id": material_id,
        })
        return material

    def get_all_materials(self, title_query, category_query, tag_query) -> Optional[QuerySet[Material]]:
        return self.material_accessors.get_all_materials(title_query, category_query, tag_query)

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
