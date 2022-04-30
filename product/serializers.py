from rest_framework import serializers
from .models import ProductTypeOne, Brand, Category


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = ProductTypeOne
        fields = ['name', 'brand', 'categories', 'price', 'quantity', 'description']
