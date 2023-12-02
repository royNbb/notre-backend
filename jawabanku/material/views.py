from rest_framework.viewsets import ViewSet

from .serializers import MaterialSerializer
from common.utils import error_response_format
from common.utils import success_response_format
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet
from .services import MaterialServices


class MaterialViewSet(ViewSet):
    material_service = MaterialServices()

    def list(self, request) -> Response:
        try:
            materials = self.material_service.get_all_materials()
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
            material = self.material_service.get_material_by_id(pk)

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
