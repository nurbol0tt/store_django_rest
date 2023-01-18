from django.contrib import admin

from product.models import Product, Manufacturer, Comment, RatingStar, Rating, Color, Category

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Color)
admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'created')
    search_fields = ('id', 'title')
    ordering = ('-created',)


admin.site.register(Product, ProductAdmin)

admin.site.register(Comment)
admin.site.register(RatingStar)
admin.site.register(Rating)
