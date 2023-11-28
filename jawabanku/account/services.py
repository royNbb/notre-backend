from typing import Optional

from .accessors import AccountAccessors
from .models import Account
from .serializers import AccountUpdateSerializer


class AccountServices:
    account_accessors = AccountAccessors()

    def update_profile(self, account: Account, **kwargs) -> Optional['Account']:

        parsed_data = {}
        if kwargs.get('name', None):
            parsed_data['name'] = kwargs.get('name')
        if kwargs.get('email', None) is not None:
            parsed_data['email'] = kwargs.get('email')
        if kwargs.get('username', None) is not None:
            parsed_data['username'] = kwargs.get('username')

        serialized_req = AccountUpdateSerializer(data=parsed_data, many=False)
        if serialized_req.is_valid():
            data = serialized_req.data
            return self.account_accessors.update_profile(account, **data)

        return None
