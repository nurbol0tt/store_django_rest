from django.db import models


class DeliveryOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]

    delivery_name = models.CharField(
        verbose_name="delivery_name",
        max_length=255,
    )
    delivery_price = models.DecimalField(
        verbose_name="delivery price",
        max_digits=9,
        decimal_places=2,
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name="delivery_method",
        max_length=255,
    )
    delivery_timeframe = models.CharField(
        verbose_name="delivery timeframe",
        max_length=255,
    )

    order = models.IntegerField(verbose_name="list order", default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Delivery Option"
        verbose_name_plural = "Delivery Options"

    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    """
    Store payment options
    """

    name = models.CharField(
        verbose_name="name",
        help_text="Required",
        max_length=255,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Payment Selection"
        verbose_name_plural = "Payment Selections"

    def __str__(self):
        return self.name
