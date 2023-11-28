from django.contrib.admin import AdminSite


class JawabanKuAdminSite(AdminSite):
    site_header = 'JawabanKu Admin'
    enable_nav_sidebar = False
