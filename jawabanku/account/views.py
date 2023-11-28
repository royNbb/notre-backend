from common.utils import error_response_format
from common.utils import success_response_format
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.viewsets import ViewSet

from .permissions import IsAccountOwner
from .serializers import AccountSerializer
from .services import AccountServices


class AccountViewSet(ViewSet):
    account_service = AccountServices()

    @action(methods=['POST'], detail=False, url_path='update', permission_classes=[IsAccountOwner])
    def update_profile(self, request) -> Response:
        try:
            account = self.account_service.update_profile(request.user, **request.data)
            serializer = AccountSerializer(account, many=False)
            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    @action(methods=['POST'], detail=False, url_path='change-password', permission_classes=[IsAccountOwner])
    def change_password(self, request) -> Response:
        old_password: str = request.data.get('old_password', None)
        new_password: str = request.data.get('new_password', None)

        if old_password is None or new_password is None:
            return error_response_format('Data incomplete', HTTP_400_BAD_REQUEST)

        try:
            self.account_service.change_password(request.user, old_password, new_password)
            return success_response_format({'message': 'Successfully changed password'}, HTTP_200_OK)

        except PermissionDenied as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_403_FORBIDDEN,
            )

        except (ValidationError, PermissionDenied) as e:
            return error_response_format(str(e), HTTP_400_BAD_REQUEST)
