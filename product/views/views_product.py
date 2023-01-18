from django.core.paginator import Paginator
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.serializers import ProductDetailSerializer, ProductListSerializer, \
    ProductUpdateSerializer, ProductCreateSerializer


class ProductListView(APIView):
    """
    Product List in pagination of ten pages
    """

    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 10)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        serializer = ProductListSerializer(page_obj, many=True)
        return Response(serializer.data)


class ProductCreateView(APIView):
    """
    Product Create, the person who registered
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = ProductCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    Product in Detail
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        """
        The algorithm shows the average rating of the product
        """

        try:
            return Product.objects.annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            ).get(pk=pk)

        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        When the page is refreshed, the counter(views) of views is added +1
        """
        snippet = self.get_object(pk)
        snippet.views += 1
        snippet.save()

        related_products = Product.objects.filter(category=snippet.category).filter(category=snippet.category)

        serializer = ProductDetailSerializer(snippet)

        if not related_products:
            return Response({'error': "category does not exist"})
        else:
            return Response({
                "product": serializer.data,
                "Related Products": ProductListSerializer(related_products, many=True).data
            }
            )


class ProductUpdateView(APIView):
    """
    When updating a product, only the creator can update
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):
        snippet = get_object_or_404(Product, id=pk)
        sn = Product(user=self.request.user)
        serializer = ProductUpdateSerializer(snippet, data=request.data)
        if request.user == snippet.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"you are not author"}, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    """
    When deleting a product, only the creator can delete
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, format=None):
        snippet = get_object_or_404(Product, id=pk)

        if request.user == snippet.user:
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"you are not author"}, status=status.HTTP_400_BAD_REQUEST)
