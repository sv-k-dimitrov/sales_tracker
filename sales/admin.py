from django.contrib import admin
from .models import Product, SalesRecord


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    search_fields = ['name', 'category']


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity_sold', 'total_sales_amount', 'date_of_sale']
    list_filter = ['date_of_sale', 'product__category']
    search_fields = ['product__name']
