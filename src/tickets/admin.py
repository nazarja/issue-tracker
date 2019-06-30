from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'username', 'slug', 'cost',  'votes', 'updated_on',)


admin.site.register(Ticket, TicketAdmin)
