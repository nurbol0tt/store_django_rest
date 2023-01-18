from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .models import Cart, CartProduct
from .serializers import CartSerializer


class AddToCartView(APIView):

    def post(self, request, pro_id):
        # get product id from requesst url
        product_obj = Product.objects.get(id=pro_id)

        cart_id = self.request.session.get("cart_id", None)

        # check if cart exists
        if cart_id:
            cart_obj = get_object_or_404(Cart, id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                 product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()

            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, image=product_obj.image, product=product_obj,
                    quantity=1, rate=product_obj.price, subtotal=product_obj.price)

                cart_obj.total += product_obj.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0, customer=request.user)
            self.request.session['cart_id'] = cart_obj.id

            cartproduct = CartProduct.objects.create(
                cart=cart_obj, image=product_obj.image, product=product_obj, quantity=1,
                subtotal=product_obj.price, rate=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return Response(status=201)


class UpdateCartItemView(APIView):
    """Update quantity"""

    def post(self, request, pro_id):
        p_qty = request.data['quantity']  # get a quantity

        cart_pro = CartProduct.objects.filter(product=pro_id)  # get product
        """
        We get the quantity of products and add this amount
        """
        for cart in cart_pro:
            cart.quantity += p_qty
            cart.subtotal += p_qty * cart.rate
            cart.save()

        return Response(status=200)


class ManageCartView(APIView):

    def post(self, request, pro_id):

        action = request.data["action"]
        cp_obj = CartProduct.objects.get(id=pro_id)
        cart_obj = cp_obj.cart

        if action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return Response(status=200)


class CartListView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            cart = CartProduct.objects.filter(cart__customer=request.user)
            serializer = CartSerializer(cart, many=True)

            total_sum = sum([i.subtotal for i in cart])

            return Response({"products": serializer.data, "total amount": total_sum})
        else:
            return Response("you are logged out or you dont have orders")
