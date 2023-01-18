from rest_framework import serializers

from payment.models import DeliveryOptions


class DeliveryChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryOptions
        fields = '__all__'
