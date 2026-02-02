from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from wine.filters import WineFilter
from wine.models import Wine, Country, Category, Mood, Purpose, WineType
from wine.serializers import (
    WineListSerializer,
    WineRetrieveSerializer,
    CountrySerializer,
    CategorySerializer,
    MoodSerializer,
    PurposeSerializer,
    WineTypeSerializer,
)


class WineListView(generics.ListAPIView):
    queryset = Wine.objects.all().distinct()
    serializer_class = WineListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WineFilter
    ordering_fields = ["price", "name"]
    ordering = [
        "price",
    ]


class WineDetailView(generics.RetrieveAPIView):
    queryset = Wine.objects.select_related(
        "country", "wine_type", "category", "purpose"
    ).prefetch_related("moods")
    serializer_class = WineRetrieveSerializer


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all().order_by("name")
    serializer_class = CountrySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class MoodListAPIView(generics.ListAPIView):
    queryset = Mood.objects.all().order_by("name")
    serializer_class = MoodSerializer


class PurposeListAPIView(generics.ListAPIView):
    queryset = Purpose.objects.all().order_by("name")
    serializer_class = PurposeSerializer


class WineTypeListAPIView(generics.ListAPIView):
    queryset = WineType.objects.all().order_by("name")
    serializer_class = WineTypeSerializer
