from django.contrib import admin
from .models import Order
from django.utils.html import format_html

class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'flower', 'quantity', 'status', 'action_icon', 'delivery_date')

    def action_icon(self, obj):
        if obj.status == 'pending':
            return format_html('<span style="color: red;">❌</span>')
        else:
            return format_html('<span style="color: green;">✅</span>')

    action_icon.short_description = 'Action'

admin.site.register(Order, OrderAdmin)
