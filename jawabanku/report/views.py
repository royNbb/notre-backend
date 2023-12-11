from email import message
import re
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from requests import Response
from common.utils import error_response_format, success_response_format
from report.models import Report

from report.serializers import ReportSerializer
from .service import ReportService
from rest_framework.viewsets import ViewSet

import traceback

# Create your views here.


class ReportViewSet(ViewSet):
    report_service = ReportService()

    @action(methods=["GET"], detail=False, url_path="read")
    def get_user_report(self, request) -> Response:
        try:
            reports = self.report_service.get_reports_on_account(request.user)
            serializer = ReportSerializer(reports, many=True)
            return success_response_format(
                data=serializer.data,
                status_code=HTTP_200_OK,
            )  # type: ignore
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )  # type: ignore

    @action(methods=["POST"], detail=False, url_path="create")
    def create_report(self, request) -> Response:
        try:
            report = self.report_service.create_report(request.user, **request.data)
            if report:
                serializer = ReportSerializer(report, many=False)
                return success_response_format(
                    data=serializer.data,
                    status_code=HTTP_200_OK,
                )  # type:ignore
            else:
                return error_response_format(
                    message="Failed to create report",
                    status_code=HTTP_400_BAD_REQUEST,
                )  # type:ignore
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )  # type:ignore

    @action(methods=["PUT"], detail=True, url_path="update")
    def update_report(self, request, pk=None) -> Response:
        status = request.data["status"]
        try:
            updated_report = self.report_service.update_report(status, pk)
            if updated_report:
                serializer = ReportSerializer(updated_report, many=False)
                return success_response_format(
                    data=serializer.data,
                    status_code=HTTP_200_OK,
                )  # type:ignore
            else:
                return error_response_format(
                    message="Failed to update report",
                    status_code=HTTP_400_BAD_REQUEST,
                )  # type:ignore
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )  # type:ignore

    @action(methods=["DELETE"], detail=True, url_path="delete")
    def delete_report(self, request, pk=None) -> Response:
        try:
            deleted_report = self.report_service.delete_report(pk)
            if deleted_report:
                serializer = ReportSerializer(deleted_report, many=False)
                return success_response_format(
                    data=serializer.data, status_code=HTTP_200_OK
                )  # type:ignore
            else:
                return error_response_format(
                    message="Failed to delete report",
                    status_code=HTTP_400_BAD_REQUEST,
                )  # type:ignore
        except Exception as e:
            return error_response_format(
                message=str(e),
                status_code=HTTP_400_BAD_REQUEST,
            )  # type:ignore
