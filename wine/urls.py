from django.urls import path
from wine.views import WineListView, WineDetailView

urlpatterns = [
    path("wines/", WineListView.as_view(), name="wine-list"),
    path("wines/<int:pk>/", WineDetailView.as_view(), name="wine-detail"),
]
app_name = "wine"
