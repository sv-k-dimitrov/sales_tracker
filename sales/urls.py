from django.urls import path
from .views import SalesRecordListView, SalesAggregateView

urlpatterns = [
    path('sales-data/', SalesRecordListView.as_view(), name='sales-data-list'),
    path('sales-data/aggregate/', SalesAggregateView.as_view(), name='sales-data-aggregate'),
]
