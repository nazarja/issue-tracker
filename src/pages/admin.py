from django.contrib import admin
from django.contrib.auth.decorators import login_required

"""
Django All-Auth requires login to main site before using django's admin.
"""
admin.site.login = login_required(admin.site.login)
