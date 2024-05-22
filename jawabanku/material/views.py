from rest_framework.viewsets import ViewSet

import os

from .serializers import CategorySerializer, MaterialSerializer, TagSerializer
from common.utils import error_response_format
from common.utils import success_response_format
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet
from .services import CategoryServices, FileUploadService, MaterialServices, TagServices
from .permissions import IsMaterialOwner
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ValidationError


class FileUploadViewSet(ViewSet):
    parser_classes = [MultiPartParser]
    file_upload_service = FileUploadService()

    def create(self, request):
        try:
            BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
            file_obj = request.data['file']

            file_data = FileUploadService.upload_file(file_obj, BUCKET_NAME)

            return success_response_format(
                data=file_data,
                status_code=HTTP_200_OK,
            )
        except ValidationError as ve:
            return error_response_format(
                message=str(ve.message),
                status_code=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )


class TagViewSet(ViewSet):
    tag_service = TagServices()

    def list(self, request) -> Response:
        try:
            tags = self.tag_service.get_all_tags()
            serializer = TagSerializer(tags, many=True)

            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None) -> Response:
        try:
            tag = self.tag_service.get_tag_by_id(pk)

            if not tag:
                return error_response_format(
                    message=f" tag with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            serializer = TagSerializer(tag)
            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )


class CategoryViewSet(ViewSet):
    category_service = CategoryServices()

    def list(self, request) -> Response:
        try:
            categories = self.category_service.get_all_categories()
            serializer = CategorySerializer(categories, many=True)

            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None) -> Response:
        try:
            category = self.category_service.get_category_by_id(pk)

            if not category:
                return error_response_format(
                    message=f" category with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            serializer = CategorySerializer(category)
            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )


class MaterialViewSet(ViewSet):
    material_service = MaterialServices()
    permission_classes = [IsMaterialOwner]

    def list(self, request) -> Response:
        try:
            title_query = self.request.query_params.get('title', "")
            category_query = self.request.query_params.getlist('category', [])
            tag_query = self.request.query_params.getlist('tag', [])

            materials = self.material_service.get_all_materials(title_query, category_query, tag_query)

            serializer = MaterialSerializer(materials, many=True)

            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None) -> Response:
        try:
            material = self.material_service.get_material_by_id(request.user, pk)

            if not material:
                return error_response_format(
                    message=f" material with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            serializer = MaterialSerializer(material)
            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def create(self, request) -> Response:
        try:
            material = self.material_service.create_material(request.user, **request.data)
            if material:
                serializer = MaterialSerializer(material)
                return success_response_format(
                    data=serializer.data,
                    status_code=HTTP_201_CREATED,
                )
            else:
                return error_response_format(
                    message="Failed to create material",
                    status_code=HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def update(self, request, pk=None) -> Response:
        try:
            material = self.material_service.get_material_by_id(request.user, pk)
            if not material:
                return error_response_format(
                    message=f" material with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            self.check_object_permissions(request, material)

            material = self.material_service.update_material(material, **request.data)
            if material:
                serializer = MaterialSerializer(material)
                return success_response_format(
                    data=serializer.data,
                    status_code=HTTP_200_OK,
                )
            else:
                return error_response_format(
                    message="Failed to update material",
                    status_code=HTTP_400_BAD_REQUEST,
                )
        except PermissionDenied as e:
            return error_response_format(
                message="You do not have permission to update this material",
                status_code=HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None) -> Response:
        try:
            material = self.material_service.get_material_by_id(request.user, pk)
            if not material:
                return error_response_format(
                    message=f" material with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            self.check_object_permissions(request, material)

            material = self.material_service.delete_material(material)
            if material:
                return Response(
                    status=HTTP_204_NO_CONTENT,
                )
            else:
                return error_response_format(
                    message="Failed to delete material",
                    status_code=HTTP_400_BAD_REQUEST,
                )
        except PermissionDenied as e:
            return error_response_format(
                message="You do not have permission to delete this material",
                status_code=HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )
