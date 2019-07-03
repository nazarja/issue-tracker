from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'username', 'slug', 'votes', 'updated_on', 'vote_profiles',)
    filter_horizontal = ('vote_profiles',)


admin.site.register(Ticket, TicketAdmin)
