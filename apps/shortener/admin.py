from django.contrib import admin
from apps.shortener.models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'short_code', 'created_at')
    search_fields = ('url', 'short_code')
    readonly_fields = ('created_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('short_code',)
        return self.readonly_fields
