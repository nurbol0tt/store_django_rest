import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Product
from .models import User

from product.serializers import ProductListSerializer
from product.service import get_client_ip
from user.serializers import RegisterSerializer, UserSerializer, CreateRatingUserSerializer, PasswordSerializer, \
    EmailVerificationSerializer, MyWishlistSerializer


class RegisterView(APIView):

    serializers = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        # get the user's email
        user = User.objects.get(email=user_data['email'])
        # This refresh token so we can create a token, then give it a user
        token = RefreshToken.for_user(user).access_token
        # get the website domain and current site
        current_site = get_current_site(request).domain
        relativeLink = reverse('email_verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user.username + \
                     ' Use the link below to verify your email \n' + absurl

        # call send method
        send_mail('Verify you Email',
                  email_body,
                  'settings.EMAIL_HOST_USERNAME',
                  [serializer.data['email']])

        return Response(serializer.data)


class EmailVerify(APIView):
    serializers = EmailVerificationSerializer

    """specify the parameter"""
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        # get token
        token = request.GET.get('token')

        try:
            # decode token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # from db get user
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": "Successfully activated "}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as _ex:
            return Response({"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as _ex:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):

    def get(self, request):
        users = User.objects.all()
        paginator = Paginator(users, 10)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        serializer = UserSerializer(page_obj, many=True)
        return Response(serializer.data)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request):
        serializer = PasswordSerializer(data=request.data)
        user = self.request.user

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):

    def get_object(self, pk):
        try:
            # do math calculation
            return User.objects.annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            ).get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        # get user products
        products = Product.objects.filter(user=user)

        serializer = UserSerializer(user)

        if not user:
            return Response({'error': "user does not exist"})
        else:
            return Response({
                "user": serializer.data,
                "count products": products.count(),
                "all products": ProductListSerializer(products, many=True).data
            }
            )


class AddStarRatingUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateRatingUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class WishlistCreateView(APIView):
    """
    Add product to wishlist
    """

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
        else:
            product.users_wishlist.add(request.user)
        return Response(status=200)


class MyWishlistView(APIView):
    """
    Show a person his saved products
    """
    def get(self, request):
        wishlist = Product.objects.filter(users_wishlist=request.user)
        serializers = MyWishlistSerializer(wishlist, many=True)
        return Response(serializers.data)
