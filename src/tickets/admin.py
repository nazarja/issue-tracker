from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    """
    create readonly fields for visibility, staff should not be able to edit certain fields
    manytomany field should be viewable as a horizontal field list
    """
    readonly_fields = ('id', 'user', 'username', 'slug', 'votes', 'updated_on', 'vote_profiles',)
    filter_horizontal = ('vote_profiles',)


admin.site.register(Ticket, TicketAdmin)
