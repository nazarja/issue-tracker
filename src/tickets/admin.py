from django.contrib import admin
from .models import Bug, Feature


class BugAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'slug', 'votes', 'view_count', 'updated_on',)


class FeatureAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'slug', 'votes', 'view_count', 'updated_on',)


admin.site.register(Bug, BugAdmin)
admin.site.register(Feature, FeatureAdmin)