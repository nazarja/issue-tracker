from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    """
    need readonly fields to be viewable in admin
    """
    readonly_fields = ('id', 'user', 'username', 'updated_on',)


admin.site.register(Comment, CommentAdmin)
