from django.contrib import admin
from .base_models import Log


class LogAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Type of modification', {'fields': ['log_text']}),
        ('Date information', {'fields': ['log_date']}),
    ]
    list_display = ('log_text', 'log_date', 'was_modified_recently')
    list_filter = ['log_date']
    search_fields = ['log_text']

admin.site.register(Log, LogAdmin)
