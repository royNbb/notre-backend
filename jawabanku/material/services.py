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
from google.cloud import storage
from google.oauth2 import service_account
from django.conf import settings

import os
import uuid
import boto3

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'ipynb', 'py', 'java', 'jav', 'c', 'cpp', 'cs', 'go', 'js', 'ts', 'jsx', 'tsx', 'html', 'css', 'php', 'sql', 'swift', 'rb', 'json', 'xml', }
MAX_FILE_SIZE_MB = 20


class FileUploadService:
    def upload_file(file_obj, bucket_name):
        try:
            random_hex = uuid.uuid4().hex

            file_extension = file_obj.name.split('.')[-1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                raise ValidationError("Invalid file extension.")

            max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
            if file_obj.size > max_size_bytes:
                print('ukuran file')
                raise ValidationError("File size exceeds the maximum allowed.")

            object_name = f'{random_hex}-{file_obj.name}'

            content_type, _ = guess_type(file_obj.name)
            content_type = content_type or 'application/octet-stream'

            # Initialize a GCS client
            print('masu')
            # Get credentials and bucket name from settings
            credentials = settings.GS_CREDENTIALS
            bucket_name = settings.GS_BUCKET_NAME

            # Initialize a GCS client with credentials
            storage_client = storage.Client(credentials=credentials)

            # Get the bucket
            bucket = storage_client.bucket(bucket_name)

            # Create a new blob
            blob = bucket.blob(object_name)

            # Debugging prints
            print(f"Uploading file: {file_obj.name}")
            print(f"Object name: {object_name}")
            print(f"Content type: {content_type}")
            
            # Check if the file_obj is a readable file-like object
            if hasattr(file_obj, 'read'):
                print("File object is a readable file-like object.")
            else:
                raise ValueError("Provided file object is not readable.")
            
            # Ensure the file pointer is at the beginning
            file_obj.seek(0)

            # Upload the file content
            blob.upload_from_file(file_obj, content_type=content_type)

            # Construct the public URL manually
            file_url = f"https://storage.googleapis.com/{bucket_name}/{object_name}"
            
            return {
                "file_url": file_url,
                "content_type": content_type
            }
        except ValidationError as ve:
            raise ve
        except Exception as e:
            print(f"Error during file upload: {e}")
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
