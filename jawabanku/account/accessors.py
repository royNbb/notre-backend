from django.db import transaction

from .models import Account


class AccountAccessors:
    def update_profile(self, account: Account, **validated_data) -> 'Account':
        with transaction.atomic():
            for key, value in validated_data.items():
                setattr(account, key, value)

            account.save()
            return account

    def change_password(self, account: Account, new_password: str) -> None:
        account.set_password(new_password)
        account.save()
