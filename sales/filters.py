import django_filters
from .models import SalesRecord


class SalesRecordFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="date_of_sale", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="date_of_sale", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="product__category")

    class Meta:
        model = SalesRecord
        fields = ['start_date', 'end_date', 'category']
