import django_filters
from wine.models import Wine


class WineFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    mood = django_filters.CharFilter(field_name="moods__name", lookup_expr="iexact")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="iexact")
    purpose = django_filters.CharFilter(field_name="purpose__name", lookup_expr="iexact")

    class Meta:
        model = Wine
        fields = ["name", "mood", "max_price", "min_price", "category", "purpose"]
