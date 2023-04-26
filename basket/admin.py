from django.contrib import admin

from basket.models import CartProduct, Cart, PurchasesHistory

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(PurchasesHistory)
