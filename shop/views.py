from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class ProductListView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, category_slug=None):
        # Initialize variables
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        # Filter products by category if category_slug is provided
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)

        # Serialize categories and products
        category_serializer = CategorySerializer(category) if category else None
        categories_serializer = CategorySerializer(categories, many=True)
        product_serializer = ProductSerializer(products, many=True)

        # Combine category, categories, and products data
        data = {
            "category": category_serializer.data if category_serializer else None,
            "categories": categories_serializer.data,
            "products": product_serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, pk, slug):
        product_queryset = Product.objects.get(pk=pk, slug=slug, available=True)
        product_serializer = self.serializer_class(product_queryset)
        data = {"product": product_serializer.data}

        return Response(data, status=status.HTTP_200_OK)
