from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from .serializer import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .models import Product
from django.core.cache import cache
from django.utils import timezone


class ProductPagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 10


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', )
    search_fields = ('name',)
    pagination_class = ProductPagination
    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        queryset = Product.objects.all()
        if on_sale is None:
            return super().get_queryset()
        if on_sale.lower() == 'true':
            now = timezone.now()
            return queryset.filter(sale_start__lte=now, sale_end__gte=now)
        if on_sale.lower() == 'false':
            now = timezone.now()
            return queryset.filter(sale_end__lte=now)
        return queryset


class ProductCreateView(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is None and float(price) <= 0.0:
                raise ValidationError({'price': 'Price should be greater than Zero'})
        except ValueError:
                raise ValidationError({'price': 'Price should be valid number'})
        return super().create(request, *args, **kwargs)


class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete('product_{}'.format(product_id))
        return response


class ProductRetrieveDestroyUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete('product_{}'.format(product_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            product = response.data
            cache.set('product_data_set_{}'.format(product['id']),
                      {'name': product['name'],
                       'description': product['description'],
                       'price': product['price']})
        return response
