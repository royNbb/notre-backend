from django.shortcuts import render

from rest_framework.viewsets import ViewSet

from .serializers import CommentSerializer
from common.utils import error_response_format
from common.utils import success_response_format
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet
from .services import CommentServices
from .permissions import IsCommentOwner
from rest_framework.exceptions import PermissionDenied



# Create your views here.
class CommentViewSet(ViewSet):
    comment_service = CommentServices()
    permission_classes = [IsCommentOwner]

    def list(self, request) -> Response:
        try:
            is_by_owner_query = self.request.query_params.get('is_by_owner', "")

            if is_by_owner_query:
                #get by owner 
                try:
                    owner_query = self.request.query_params.get('owner', "")
                    comments = self.comment_service.get_comments_by_owner(owner_query)

                    serializer = CommentSerializer(comments, many=True)

                    return success_response_format(
                        data=serializer.data,
                        status_code=HTTP_200_OK,
                    )
                except Exception as e:
                    return error_response_format(
                        message=str(e),
                        status_code=HTTP_400_BAD_REQUEST,
                    )
            else:
                #get by material comments
                try:
                    material_query = self.request.query_params.get('material', "")
                    comments = self.comment_service.get_comments_by_material(material_query)

                    serializer = CommentSerializer(comments, many=True)

                    return success_response_format(
                        data=serializer.data,
                        status_code=HTTP_200_OK,
                    )
                except Exception as e:
                    return error_response_format(
                        message=str(e),
                        status_code=HTTP_400_BAD_REQUEST,
                    )                
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None) -> Response:
        try:
            comment = self.comment_service.get_comment_by_id(pk)

            if not comment:
                return error_response_format(
                    message=f" comment with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            serializer = CommentSerializer(comment)
            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def create(self, request) -> Response:
        try:
            comment = self.comment_service.create_comment(request.user, **request.data)
            if comment:
                serializer = CommentSerializer(comment)
                print('METHOD CREATE SUCCESS IN VIEWS')
                print(serializer.data)
                return success_response_format(
                    data=serializer.data,
                    status_code=HTTP_201_CREATED,
                )
            else:
                print('METHOD CREATE GO TO ELSE ERROR RESPONSE FORMAT IN VIEWS')
                
                return error_response_format(
                    message="Failed to create comment",
                    status_code=HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print('METHOD CREATE GO TO EXCEPTION ERROR RESPONSE FORMAT IN VIEWS')

            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def update(self, request, pk=None) -> Response:
        try:
            comment = self.comment_service.get_comment_by_id(pk)
            if not comment:
                return error_response_format(
                    message=f" comment with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            self.check_object_permissions(request, comment)

            comment = self.comment_service.update_comment(comment, **request.data)
            if comment:
                serializer = CommentSerializer(comment)
                return success_response_format(
                    data=serializer.data,
                    status_code=HTTP_200_OK,
                )
            else:
                return error_response_format(
                    message="Failed to update comment",
                    status_code=HTTP_400_BAD_REQUEST,
                )
        except PermissionDenied as e:
            return error_response_format(
                message="You do not have permission to update this comment",
                status_code=HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None) -> Response:
        try:
            comment = self.comment_service.get_comment_by_id(pk)
            if not comment:
                return error_response_format(
                    message=f" comment with ID {pk} not found",
                    status_code=HTTP_404_NOT_FOUND,
                )

            self.check_object_permissions(request, comment)

            comment = self.comment_service.delete_comment(comment)
            if comment:
                return Response(
                    status=HTTP_204_NO_CONTENT,
                )
            else:
                return error_response_format(
                    message="Failed to delete comment",
                    status_code=HTTP_400_BAD_REQUEST,
                )
        except PermissionDenied as e:
            return error_response_format(
                message="You do not have permission to delete this comment",
                status_code=HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )
