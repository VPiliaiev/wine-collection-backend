from django.urls import path
from wine.views import (
    WineListView,
    WineDetailView,
    CountryListAPIView,
    CategoryListAPIView,
    MoodListAPIView,
    PurposeListAPIView,
    WineTypeListAPIView,
)

urlpatterns = [
    path("wines/", WineListView.as_view(), name="wine-list"),
    path("wines/<int:pk>/", WineDetailView.as_view(), name="wine-detail"),
    path("countries/", CountryListAPIView.as_view(), name="country-list"),
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("moods/", MoodListAPIView.as_view(), name="mood-list"),
    path("purposes/", PurposeListAPIView.as_view(), name="purpose-list"),
    path("wine-types/", WineTypeListAPIView.as_view(), name="wine-type-list"),
]
app_name = "wine"
