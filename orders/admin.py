from django.contrib import admin
from . import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer_name', 'flower_name', 'delivery_address', 'quantity', 'order_status', 'order_types', 'mobile_no', 'order_date', 'delivery_date', 'cancel','paid')

    def buyer_name(self, obj):
        return obj.buyer.user.first_name

    def flower_name(self, obj):
        return obj.flower.title

    def save_model(self, request, obj, form, change):
        # Save the order
        obj.save()

        # Check if order status has changed and send an email notification
        if change:
            email_subject = f"Your Order Status: {obj.order_status}"
            email_body = render_to_string('admin_email.html', {
                'user': obj.buyer.user,
                'order_id': obj.id,
                'status': obj.order_status,
            })

            email = EmailMultiAlternatives(
                email_subject,
                '',
                to=[obj.buyer.user.email]
            )
            email.attach_alternative(email_body, "text/html")
            email.send()

    
admin.site.register(models.Order, OrderAdmin)

