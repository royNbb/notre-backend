from typing import Optional

from account.models import Account
from .serializers import CreateCommentSerializer, UpdateCommentSerializer
from .models import Comment
from .accessors import CommentAccessors
from django.db.models import QuerySet

class CommentServices:
    comment_accessors = CommentAccessors()

    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        return self.comment_accessors.get_comment_by_id(comment_id)

    def get_comments_by_owner(self, owner_query) -> Optional[QuerySet[Comment]]:
        return self.comment_accessors.get_comments_by_owner(owner_query)

    def get_comments_by_material(self, material_query) -> Optional[QuerySet[Comment]]:
        return self.comment_accessors.get_comments_by_material(material_query)

    def create_comment(self, account: Account, **kwargs) -> Optional[Comment]:
        parsed_data = {}
        parsed_data['owner_id'] = account.id
        print(account.id)
        if kwargs.get('material', None):
            parsed_data['material'] = kwargs.get('material')
            print(f'Material {parsed_data["material"]}')
        if kwargs.get('content', None):
            parsed_data['content'] = kwargs.get('content')
            print(f'Content {parsed_data["content"]}')

        serialized_req = CreateCommentSerializer(data=parsed_data, many=False)
        if serialized_req.is_valid():
            print('SUCCESS')
            data = serialized_req.validated_data
            return self.comment_accessors.create_comment(account, **data)

        return None

    def update_comment(self, comment: Comment, **kwargs) -> Optional[Comment]:
        parsed_data = {}
        if kwargs.get('content', None):
            parsed_data['content'] = kwargs.get('content')

        serialized_req = UpdateCommentSerializer(data=parsed_data, many=False)
        if serialized_req.is_valid():
            data = serialized_req.validated_data
            return self.comment_accessors.update_comment(comment, **data)

        return None

    def delete_comment(self, comment: Comment) -> None:
        return self.comment_accessors.delete_comment(comment)
