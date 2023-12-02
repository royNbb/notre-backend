from typing import Optional

from account.models import Account

from django.db.models import QuerySet

from .models import UserHistory
from .serializers import CreateUserHistorySerializer
from .accessors import HistoryAccessor


class HistoryService:
  history_accessor = HistoryAccessor()

  def get_history_of_account(self, account: Account) -> Optional[QuerySet['UserHistory']]:
    return self.history_accessor.get_history_of_account(account)

  def create_history(self, account: Account, **kwargs) -> Optional['UserHistory']:
    """Create History for a User
    Pass along a dictionary containing, related_model_app_label, related_model_name, related_model_id
    owner_id will be infered from account, so just pass along request.user
    Example Usage:
    data = {
      "related_model_app_label": "comment",
      "related_model_name": "comment",
      "related_model_id": 2, // this specifies the comment id which we are making the history of
    }
    create_history(request.user, **data)
    """
    parsed_data = {}
    parsed_data['owner_id'] = account.id
    if kwargs.get('related_model_app_label', None):
      parsed_data['related_model_app_label'] = kwargs.get('related_model_app_label')
    if kwargs.get('related_model_name', None):
      parsed_data['related_model_name'] = kwargs.get('related_model_name')
    if kwargs.get('related_model_id', None):
      parsed_data['related_model_id'] = kwargs.get('related_model_id')

    serialized_req = CreateUserHistorySerializer(data=parsed_data, many=False)
    if serialized_req.is_valid():
      data = serialized_req.data
      return self.history_accessor.create_history(account, **data)

    return None
