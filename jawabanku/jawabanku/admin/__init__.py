from .base import JawabanKuAdminSite

admin_site = JawabanKuAdminSite(name='jawabankuadmin')


from django.contrib.admin.models import LogEntry  # noqa
from django_admin_logs.admin import LogEntryAdmin  # noqa

admin_site.register(LogEntry, LogEntryAdmin)

from account.admin import *  # noqa
from material.admin import *  # noqa
from report.admin import *  # noqa
from comment.admin import *  # noqa
from history.admin import *  # noqa
