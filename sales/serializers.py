from rest_framework import serializers
from .models import Product, SalesRecord


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price']


class SalesRecordSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SalesRecord
        fields = ['id', 'product', 'quantity_sold', 'total_sales_amount', 'date_of_sale']


class SalesAggregateSerializer(serializers.Serializer):

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if instance.get('product__category', None):
            data['category'] = instance.get('product__category')
        else:
            data['month'] = instance.get('month').strftime('%Y-%m')

        data['total_sales'] = instance.get('total_sales')
        data['average_price'] = instance.get('average_price')

        return data
