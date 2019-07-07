from django.contrib import admin
from .models import Contact


class ContactFormAdmin(admin.ModelAdmin):
    """
    Change Admin Panel's display name for contact model,
    set readonly fields for field visibility
    """
    readonly_fields = ('user', 'sent_on',)

    class Meta:
        fields = ('user', 'name', 'message', 'subject', 'message', 'sent_on')
        verbose_name = 'Contact Form'
        verbose_name_plural = 'Contact Forms'


admin.site.register(Contact, ContactFormAdmin)
