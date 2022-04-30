import django_filters
from .models import ProductTypeOne


class ProductListFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')

    class Meta:
        model = ProductTypeOne
        fields = ['brand']
