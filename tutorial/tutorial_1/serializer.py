from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    description = serializers.CharField(min_length=2, max_length=200)
    product_name = serializers.CharField(source='name')
    sale_start = serializers.DateTimeField(
        required= False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=False,
        help_text='Accepted date format is "12:01 pm 9 dec 2022"',
        style={'input_type': 'text', 'placeholder': '12:01 pm 9 dec 2022'}
    )

    sale_end = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=False,
        help_text='Accepted date format is "12:01 pm 9 dec 2022"',
        style={'input_type': 'text', 'placeholder': '12:01 pm 9 dec 2022'}
    )


    class Meta:
        model = Product
        fields = ('id', 'product_name', 'description', 'price', 'sale_start', 'sale_end')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_on_sale'] = instance.is_on_sale()
        data['current_price'] = instance.current_price()
        return data
