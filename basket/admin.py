from django.contrib import admin

from basket.models import Basket, CartProduct, Cart, PurchasesHistory

# Register your models here.
admin.site.register(Basket)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(PurchasesHistory)
