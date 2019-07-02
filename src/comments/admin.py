from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'username', 'updated_on',)


admin.site.register(Comment, CommentAdmin)
