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

from .serializers import UserHistorySerializer
from .services import HistoryService


class HistoryViewSet(ViewSet):
  history_service = HistoryService()

  @action(methods=['GET'], detail=False, url_path='mine')
  def get_user_history(self, request) -> Response:
    try:
      history = self.history_service.get_history_of_account(request.user)
      serializer = UserHistorySerializer(history, many=True)
      return success_response_format(
          data=serializer.data,
          status_code=HTTP_200_OK,
      )
    except Exception as e:
      return error_response_format(
          message=str(e),
          status_code=HTTP_400_BAD_REQUEST,
      )
