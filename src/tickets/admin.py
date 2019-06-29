from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'slug', 'cost',  'votes', 'view_count', 'updated_on',)


admin.site.register(Ticket, TicketAdmin)
