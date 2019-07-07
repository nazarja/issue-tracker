from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    """
    prevent staff from changing important values,
    manytomany field should be visible - horizontally
    """
    readonly_fields = ('ticket', 'user', 'votes', 'total',)
    filter_horizontal = ('ticket',)


admin.site.register(Order, OrderAdmin)

