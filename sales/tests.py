from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, SalesRecord
from .serializers import SalesRecordSerializer, SalesAggregateSerializer
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Avg


class SalesRecordTestCase(APITestCase):
    def setUp(self):
        # Create products
        self.product1 = Product.objects.create(name="Product 1", category="Category 1", price=10.00)
        self.product2 = Product.objects.create(name="Product 2", category="Category 2", price=20.00)

        # Create sales records
        self.record1 = SalesRecord.objects.create(
            product=self.product1,
            quantity_sold=10,
            total_sales_amount=100.00,
            date_of_sale="2024-08-01T12:00:00Z"
        )
        self.record2 = SalesRecord.objects.create(
            product=self.product2,
            quantity_sold=20,
            total_sales_amount=400.00,
            date_of_sale="2024-08-15T12:00:00Z"
        )
        self.record3 = SalesRecord.objects.create(
            product=self.product1,
            quantity_sold=15,
            total_sales_amount=150.00,
            date_of_sale="2024-09-01T12:00:00Z"
        )

    def test_sales_record_list_view(self):
        """Test that the SalesRecordListView returns the correct list of sales records."""
        url = reverse('sales-data-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = SalesRecordSerializer(SalesRecord.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_sales_aggregate_by_category(self):
        """Test that the SalesAggregateView aggregates data by category correctly."""
        url = reverse('sales-data-aggregate')
        response = self.client.get(url, {'aggregate_by': 'category'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = SalesRecord.objects.values('product__category').annotate(
            total_sales=Sum('total_sales_amount'),
            average_price=Avg('product__price')
        ).order_by('product__category')

        expected_data = SalesAggregateSerializer(expected_data, many=True).data
        self.assertEqual(response.data, expected_data)

    def test_sales_aggregate_by_month(self):
        """Test that the SalesAggregateView aggregates data by month correctly."""
        url = reverse('sales-data-aggregate')
        response = self.client.get(url, {'aggregate_by': 'month'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = SalesRecord.objects.annotate(
            month=TruncMonth('date_of_sale')
        ).values('month').annotate(
            total_sales=Sum('total_sales_amount'),
            average_price=Avg('product__price')
        ).order_by('month')

        expected_data = SalesAggregateSerializer(expected_data, many=True).data
        self.assertEqual(response.data, expected_data)

    def test_sales_aggregate_serializer_category(self):
        """Test that the SalesAggregateSerializer correctly formats data aggregated by category."""
        data = {
            'product__category': 'Category 1',
            'total_sales': 250.00,
            'average_price': 10.00
        }
        serializer = SalesAggregateSerializer(data)
        self.assertEqual(serializer.data['category'], 'Category 1')
        self.assertEqual(serializer.data['total_sales'], 250.00)
        self.assertEqual(serializer.data['average_price'], 10.00)

    def test_sales_aggregate_serializer_month(self):
        """Test that the SalesAggregateSerializer correctly formats data aggregated by month."""
        data = {
            'month': datetime(2024, 8, 11, 20),
            'total_sales': 500.00,
            'average_price': 15.00
        }
        serializer = SalesAggregateSerializer(data)
        self.assertEqual(serializer.data['month'], "2024-08")
        self.assertEqual(serializer.data['total_sales'], 500.00)
        self.assertEqual(serializer.data['average_price'], 15.00)
