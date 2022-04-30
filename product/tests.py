from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Category, Brand, ProductTypeOne, ProductTypeTwo, ProductTypeThree
from django.urls import reverse


class ManagerTest(TestCase):
    def setUp(self):
        self.brand_1 = Brand.objects.create(name='B1')
        self.brand_2 = Brand.objects.create(name='B2')
        self.brand_3 = Brand.objects.create(name='B3')
        self.category_1 = Category.objects.create(name='C1')
        self.category_2 = Category.objects.create(name='C2')
        self.category_3 = Category.objects.create(name='C3', parent=self.category_1)
        self.category_4 = Category.objects.create(name='C4', parent=self.category_1)
        self.category_5 = Category.objects.create(name='C5', parent=self.category_2)

        self.product_1 = ProductTypeOne.objects.create(name='P1', quantity=10, price=10, brand=self.brand_1)
        self.product_1.categories.add(self.category_3, self.category_5)
        self.product_2 = ProductTypeOne.objects.create(name='P1', quantity=11, price=10, brand=self.brand_2)
        self.product_2.categories.add(self.category_4, self.category_5)
        self.product_3 = ProductTypeOne.objects.create(name='P2', quantity=1, price=10, brand=self.brand_1)
        self.product_3.categories.add(self.category_3)

        self.product_4 = ProductTypeTwo.objects.create(name='P3', quantity=20, price=10, brand=self.brand_1)
        self.product_4.categories.add(self.category_3)
        self.product_5 = ProductTypeTwo.objects.create(name='P4', quantity=20, price=10, brand=self.brand_2)
        self.product_5.categories.add(self.category_5)

        self.product_6 = ProductTypeThree.objects.create(name='P5', quantity=11, price=10.99, brand=self.brand_2)
        self.product_6.categories.add(self.category_3)

    def test_slug(self):
        self.assertEqual(self.product_1.slug, 'p1')
        self.assertNotEqual(self.product_2.slug, 'p1')

    def test_availability_manager(self):
        all_type_one_products = ProductTypeOne.objects.all()
        self.assertEqual(len(all_type_one_products), 3)

        available_type_one_products = ProductTypeOne.objects.check_availability()
        self.assertEqual(len(available_type_one_products), 1)

        available_type_one_products_category_3 = ProductTypeOne.objects.check_availability(category=self.category_3)
        self.assertEqual(len(available_type_one_products_category_3), 0)

        available_type_one_products_category_4 = ProductTypeOne.objects.check_availability(category=self.category_4)
        self.assertEqual(len(available_type_one_products_category_4), 1)

        available_type_one_products_category_5 = ProductTypeOne.objects.check_availability(category=self.category_5)
        self.assertEqual(len(available_type_one_products_category_5), 1)

        available_type_two_products = ProductTypeTwo.objects.check_availability()
        self.assertEqual(len(available_type_two_products), 2)

        available_type_three_products_brand_1 = ProductTypeThree.objects.check_availability(brand=self.brand_1)
        self.assertEqual(len(available_type_three_products_brand_1), 0)

        available_type_three_products_brand_2 = ProductTypeThree.objects.check_availability(brand=self.brand_2)
        self.assertEqual(len(available_type_three_products_brand_2), 1)


class TestProduct(APITestCase):

    def setUp(self):
        self.category_1 = Category.objects.create(name='C1')
        self.brand_1 = Brand.objects.create(name='B1')
        self.brand_2 = Brand.objects.create(name='B2')

        self.product_1 = ProductTypeOne.objects.create(name='P', quantity=10, price=10, brand=self.brand_1)
        self.product_2 = ProductTypeOne.objects.create(name='P', quantity=10, price=10, brand=self.brand_1)
        self.product_3 = ProductTypeOne.objects.create(name='P', quantity=10, price=10, brand=self.brand_2)

    def test_product_list(self):
        url = reverse('product_list') + '?brand=b'
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 3)

        url = reverse('product_list') + '?brand=1'
        resp_2 = self.client.get(url)
        self.assertEqual(len(resp_2.data), 2)
