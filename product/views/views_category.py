from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Category
from product.serializers import CategorySerializer, ProductMostPopularViewListSerializer


class CategoryListView(APIView):
    """
    list Category
    """
    def get(self, request):
        product = Category.objects.all()
        serializer = CategorySerializer(product, many=True)
        return Response(serializer.data)


class CategoryCreateView(APIView):
    """
    Only admin can create a category
    """
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """
    Category Detail
    """
    def get(self, request, pk, format=None):
        """
        Show customer similar in product
        """
        category = get_object_or_404(Category, id=pk)
        products = Product.objects.filter(category=category)

        serializer = CategorySerializer(category)

        if not category:
            return Response({'error': "category does not exist"})
        else:
            return Response({
                "category": serializer.data,
                "all products by category": ProductMostPopularViewListSerializer(products, many=True).data
            }
            )


class CategoryUpdateView(APIView):
    """
    Only admin can update Category
    """

    permission_classes = [IsAdminUser]

    def put(self, request, pk, format=None):
        snippet = get_object_or_404(Category, id=pk)
        serializer = CategorySerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    """
    Only admin can delete Category
    """
    permission_classes = [IsAdminUser]

    def delete(self, request, pk, format=None):
        snippet = get_object_or_404(Category, id=pk)
        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
