from ast import parse
import datetime
import time
from typing import Optional
from account.models import Account
from .models import Report
from .accessors import ReportAccessor
from .serializers import ReportSerializer
from django.db.models import QuerySet
from django.contrib.contenttypes.models import ContentType


class ReportService:
    report_accessor = ReportAccessor()

    def get_reports_on_account(self, account: Account) -> Optional[QuerySet["Report"]]:
        coba = self.report_accessor.get_report_of_account(account)
        return coba

    def create_report(self, account: Account, **kwargs) -> Optional["Report"]:
        parsed_data = {}
        parsed_data["owner_id"] = account.id
        if kwargs.get("related_model_app_label", None):
            parsed_data["related_model_app_label"] = kwargs.get(
                "related_model_app_label"
            )
        if kwargs.get("related_model_name", None):
            parsed_data["related_model_name"] = kwargs.get("related_model_name")
        if kwargs.get("related_model_id", None):
            parsed_data["related_model_id"] = kwargs.get("related_model_id")

        if kwargs.get("description", None):
            parsed_data["description"] = kwargs.get("description")
        parsed_data["created_at"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        serialized_req = ReportSerializer(data=parsed_data, many=False)  # type: ignore

        if serialized_req.is_valid():
            data = serialized_req.validated_data
            data["related_model_app_label"] = parsed_data.get("related_model_app_label")
            data["related_model_name"] = parsed_data.get("related_model_name")
            data["related_model_id"] = parsed_data.get("related_model_id")

            return self.report_accessor.create_report(account, **data)

        return None

    def update_report(self, status: bool, pk: int) -> Optional[Report]:
        return self.report_accessor.update_report(status, pk)

    def delete_report(self, pk: int) -> Optional[Report]:
        return self.report_accessor.delete_report(pk)
