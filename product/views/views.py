from django.core.paginator import Paginator
from django.db import models
from django.db.models.functions import Cast
from django.db.models import FloatField, Q
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.serializers import ProductListSerializer, CreateRatingSerializer, ProductMostPopularViewListSerializer

from product.service import get_client_ip


class AddStarRatingView(APIView):
    """
    Adding a rating to a product
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class LikeView(APIView):
    """
    We like a product
    """
    def post(self, request, pk):
        post = get_object_or_404(Product, id=pk)
        print(post)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return Response(status=200)


class ProductMostPopular(APIView):
    """
    See the most popular products
    """
    def get(self, request):
        """
        Here is the math
        """
        products = Product.objects.all().annotate(
            pp=Cast(models.F('number_of_sales'), output_field=FloatField()) / (Cast(models.Count(models.F('likes')),
                        output_field=FloatField()) + Cast(models.F('views'), output_field=FloatField())) * 100
        ).order_by('-pp')
        """
        (Number of sales divided by (likes + views)) * 100
        """
        # pp = [(i, i.number_of_sales / (i.likes.count() + i.views) * 100) for i in products]

        paginator = Paginator(products, 10)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        serializer = ProductMostPopularViewListSerializer(page_obj, many=True)

        return Response(serializer.data)


class ProductMostViewed(APIView):
    """
    Most Viewed Products
    """

    def get(self, request):
        """
        Get the number of views and do it in descending order
        """
        products = Product.objects.all().order_by('-views')
        paginator = Paginator(products, 10)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        serializer = ProductMostPopularViewListSerializer(page_obj, many=True)
        return Response(serializer.data)


class MostLikeView(APIView):
    """
    Most Viewed Like
    """
    def get(self, request):
        """
        Get the number of views and do it in descending order
        """
        likes = Product.objects.all().order_by('-likes')
        paginator = Paginator(likes, 10)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        serializer = ProductMostPopularViewListSerializer(page_obj, many=True)
        return Response(serializer.data)


class SearchView(APIView):
    def get(self, request):
        # search/?q=title
        """
        Get a search request from the user
        """
        q = request.GET['q']
        data = Product.objects.filter(title__icontains=q).order_by('-id')
        serializer = ProductListSerializer(data, many=True)
        return Response(serializer.data)


class FilterDataView(APIView):
    def get(self, request):
        """
        Getting the price range
        """
        minPrice = request.GET['minPrice']
        maxPrice = request.GET['maxPrice']

        allProducts = Product.objects.all().order_by('-id').distinct()

        """
        filter prices in the range from minimum to maximum
        """
        allProducts = allProducts.filter(price__gte=minPrice)
        allProducts = allProducts.filter(price__lte=maxPrice)

        """
        The received data is further filtered by manufacturer, category, color
        """
        if manufacturer := request.GET.getlist("manufacturer"):
            allProducts = allProducts.filter(manufacturer__id__in=manufacturer).distinct()
        if category := request.GET.getlist("category"):
            allProducts = allProducts.filter(category__id__in=category).distinct()
        if color := request.GET.getlist("color"):
            allProducts = allProducts.filter(color__id__in=color).distinct()

        serializer = ProductListSerializer(allProducts, many=True)
        return Response(serializer.data)
