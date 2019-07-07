from django.contrib import admin
from django.contrib.auth.decorators import login_required

"""
django all-auth requires login to main site before using django's admin.
the django admin page log in now becomes the main log in page.
after logging in, you'll be redirected to the admin page.
"""

admin.site.login = login_required(admin.site.login)
