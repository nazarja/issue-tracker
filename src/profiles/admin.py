from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    view user associated to the profile, not editable
    """
    readonly_fields = ('user',)


admin.site.register(Profile, ProfileAdmin)
