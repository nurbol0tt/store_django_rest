from rest_framework import serializers

from basket.models import CartProduct, PurchasesHistory


class CartSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = CartProduct
        fields = ('id', 'cart', 'image', 'product', 'rate', 'quantity', 'subtotal')


class PurchaseHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasesHistory
        fields = ('name', 'price', 'quantity',  'subtotal', 'datetime')

