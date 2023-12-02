from account.models import Account
from django.db.models import QuerySet
from django.contrib.contenttypes.models import ContentType

from .models import UserHistory


class HistoryAccessor:
  def get_history_of_account(self, account: Account) -> QuerySet['UserHistory']:
    return UserHistory.objects.filter(
        owner=account,
    )

  def create_history(self, account: Account, **validated_data) -> 'UserHistory':
    return UserHistory.objects.create(
        owner=account,
        content_type=ContentType.objects.get_by_natural_key(
            app_label=validated_data.get('related_model_app_label'),
            model=validated_data.get('related_model_name'),
        ),
        object_id=validated_data.get('related_model_id'),
    )
