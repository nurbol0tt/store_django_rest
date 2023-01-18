from django.contrib import admin

from payment.models import DeliveryOptions, PaymentSelections

# Register your models here.
admin.site.register(DeliveryOptions)
admin.site.register(PaymentSelections)