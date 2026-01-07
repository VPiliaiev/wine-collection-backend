from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from wine.filters import WineFilter
from wine.models import Wine
from wine.serializers import WineListSerializer, WineRetrieveSerializer


class WineListView(generics.ListAPIView):
    queryset = Wine.objects.select_related(
        "country", "wine_type", "category"
    ).prefetch_related("moods")
    serializer_class = WineListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WineFilter
    ordering = ["price"]


class WineDetailView(generics.RetrieveAPIView):
    queryset = Wine.objects.select_related(
        "country", "wine_type", "category"
    ).prefetch_related("moods")
    serializer_class = WineRetrieveSerializer
