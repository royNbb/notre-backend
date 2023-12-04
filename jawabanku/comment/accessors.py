from typing import Optional

from account.models import Account
from .models import Comment
from django.db import transaction
from django.db.models import QuerySet
from django.db.models import Q


class CommentAccessors:
    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        try:
            comment = Comment.objects.get(pk=comment_id)
            return comment
        except Comment.DoesNotExist:
            return None

    def get_comments_by_owner(self, owner_query) -> Optional[QuerySet[Comment]]:
        try:
            comments = Comment.objects.all()
            if owner_query:
                comments = comments.filter(Q(owner__exact=owner_query))
            return comments
        except Comment.DoesNotExist:
            return None
    
    def get_comments_by_material(self, material_query) -> Optional[QuerySet[Comment]]:
        try:
            comments = Comment.objects.all()
            if material_query:
                comments = comments.filter(Q(material__exact=material_query))
            return comments
        except Comment.DoesNotExist:
            return None

    def create_comment(self, account: Account, **validated_data) -> Optional[Comment]:
        try:
            comment = Comment.objects.create(
                owner=account,
                material=validated_data.get("material"),
                content=validated_data.get("content"),
            )
            comment.save()
            return comment
        except Exception as e:
            return None

    def update_comment(self, comment: Comment, **validated_data) -> Optional[Comment]:
        try:
            with transaction.atomic():
                for key, value in validated_data.items():
                    setattr(comment, key, value)
                comment.save()
                return comment
        except Exception as e:
            return None

    def delete_comment(self, comment: Comment) -> bool:
        try:
            comment.delete()
            return True
        except Exception as e:
            return False
