from django.contrib import admin
from .models import Newsletter

class NewsletterModelAdmin(admin.ModelAdmin):
    list_display = ['cusEmail', 'id', 'created_at']
    search_fields = ['cusEmail']
    list_filter = ['cusEmail']

admin.site.register(Newsletter, NewsletterModelAdmin)