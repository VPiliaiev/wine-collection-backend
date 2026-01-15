import django_filters
from wine.models import Wine


class WineFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    mood = django_filters.AllValuesMultipleFilter(field_name="moods__name")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.AllValuesMultipleFilter(field_name="category__name")
    purpose = django_filters.AllValuesMultipleFilter(field_name="purpose__name")
    country = django_filters.AllValuesMultipleFilter(field_name="country__name")

    class Meta:
        model = Wine
        fields = [
            "name",
            "mood",
            "max_price",
            "min_price",
            "category",
            "purpose",
            "country",
        ]
