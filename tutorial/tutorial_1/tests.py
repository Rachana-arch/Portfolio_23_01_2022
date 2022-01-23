from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Product

class ProductCreateTest(APITestCase):
    def test_create_product(self):
        product_count = Product.objects.count()
        attr = {"product_name": "kurti",
              "description": "It is very good.",
                "price": 250.0}
        response = self.client.post('http://127.0.0.1:8000/api/v1/product/new', attr)
        if response.status_code != 201:
            print(response)
        self.assertEqual(
            product_count+1,
            Product.objects.count(),
        )



# Create your tests here.
