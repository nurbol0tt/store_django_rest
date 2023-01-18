import stripe
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.models import CartProduct
from store import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(APIView):

    def post(self, request, pk):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        cart_pro = CartProduct.objects.get(id=pk)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            # Specify the exact price id of the product we want sell.
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': cart_pro.rate,
                        'product_data': {
                            'name': cart_pro.product.title,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "cart_id": cart_pro.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/api/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return Response(checkout_session["url"])


class MyWebhookView(APIView):

    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=400)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed' or event["type"] == "payment_intent.succeeded":
            session = event['data']['object']
            customer_email = session["customer_details"]["email"]
            # customer_email = session["email "]
            product_id = session["metadata"]["cart_id"]

            product = CartProduct.objects.get(id=product_id)

            send_mail(
                subject="Here is your product",
                message=f"Thanks for your purchase. Here is the product you ordered."
                        f" Product name: {product.product.title}",
                recipient_list=[customer_email],
                from_email="nurbolot664@gmail.com"
            )

            print("Session", session)

        return Response(status=200)


class SuccessView(APIView):

    def get(self, request):

        return Response("Payment Success")
