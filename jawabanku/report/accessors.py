from typing import Optional
from account.models import Account
from django.db.models import QuerySet
from django.contrib.contenttypes.models import ContentType

from .models import Report


class ReportAccessor:
    def create_report(self, account: Account, **validated_data) -> Optional[Report]:
        try:
            report = Report.objects.create(
                reporter=account,
                description=validated_data.get("description"),
                content_type=ContentType.objects.get(
                    app_label=validated_data.get("related_model_app_label"),  # type: ignore
                    model=validated_data.get("related_model_name"),  # type: ignore
                ),
                object_id=validated_data.get("related_model_id"),
            )
            return report
        except Exception as e:
            return None

    def get_report_of_account(self, account: Account) -> Optional[QuerySet[Report]]:
        try:
            reports = Report.objects.filter(reporter=account)
            print(reports.all())
            return reports.all()
        except Exception as e:
            return None

    def update_report(self, status: bool, pk: int) -> Optional[Report]:
        try:
            report = Report.objects.get(id=pk)
            report.status = status
            report.save()
            return report
        except Report.DoesNotExist:
            pass

    def delete_report(self, pk: int) -> Optional[Report]:
        try:
            print(pk)
            report = Report.objects.get(id=pk)
            print(report)
            report.delete()
            return report
        except Report.DoesNotExist:
            return None
