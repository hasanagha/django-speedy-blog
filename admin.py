from django.contrib import admin
from django.db import models as django_models
from pagedown.widgets import AdminPagedownWidget

from . import models


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {django_models.TextField: {'widget': AdminPagedownWidget}, }
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'created_on', 'posted_by', 'allow_comments')


class CommentAdmin(admin.ModelAdmin):
    formfield_overrides = {django_models.TextField: {'widget': AdminPagedownWidget}, }
    list_display = ('user_name', 'user_email', 'ip_address', 'created_on')


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
