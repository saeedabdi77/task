from .models import ProductTypeOne
from rest_framework import generics, mixins
from .filters import ProductListFilter
from .serializers import ProductSerializer


class ProductListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ProductTypeOne.objects.all()
    filterset_class = ProductListFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
