from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

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

    def change_password(self, account: Account, old_password: str, new_password: str) -> None:
        if authenticate(username=account.username, password=old_password) is None:
            raise PermissionDenied('The given password does not match.')

        try:
            validate_password(password=new_password, user=account)
            self.account_accessors.change_password(account, new_password)

        except ValidationError as e:
            raise e
