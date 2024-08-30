from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Sum
from .models import SalesRecord
from .serializers import SalesRecordSerializer, SalesAggregateSerializer
from .filters import SalesRecordFilter
from django.db.models.functions import TruncMonth


class SalesRecordListView(generics.ListAPIView):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesRecordFilter


class AggregationStrategy:
    def aggregate(self, queryset):
        raise NotImplementedError("Subclasses must implement this method.")


class CategoryAggregation(AggregationStrategy):
    def aggregate(self, queryset):
        return queryset.values('product__category').annotate(
            total_sales=Sum('total_sales_amount'),
            average_price=Avg('product__price')
        ).order_by('product__category')


class MonthAggregation(AggregationStrategy):
    def aggregate(self, queryset):
        return queryset.annotate(
            month=TruncMonth('date_of_sale')
        ).values('month').annotate(
            total_sales=Sum('total_sales_amount'),
            average_price=Avg('product__price')
        ).order_by('month')


class SalesAggregateView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesRecordFilter

    def get(self, request, *args, **kwargs):
        queryset = SalesRecord.objects.all()

        # Apply filters
        filterset = SalesRecordFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        queryset = filterset.qs

        # Choose aggregation strategy
        aggregate_by = request.query_params.get('aggregate_by', 'month')
        aggregation_strategy = self.get_aggregation_strategy(aggregate_by)

        # Perform aggregation
        data = aggregation_strategy.aggregate(queryset)

        # Serialize data
        serializer = SalesAggregateSerializer(data, many=True)
        return Response(serializer.data)

    def get_aggregation_strategy(self, aggregate_by):
        strategies = {
            'category': CategoryAggregation(),
            'month': MonthAggregation(),
        }
        return strategies.get(aggregate_by, MonthAggregation())
