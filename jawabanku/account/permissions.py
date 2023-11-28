from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    message = 'You are not allowed to access this resource'

    def has_permission(self, request, view) -> bool:
        account = request.user
        request_id = int(request.data.get('id', None))

        return (request_id is not None) and (account.pk == request_id)
