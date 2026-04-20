import django_filters
from wine.models import Wine, Mood, Category, Purpose, Country, WineType


class WineFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    mood = django_filters.ModelMultipleChoiceFilter(
        field_name="moods",
        queryset=Mood.objects.all(),
    )
    category = django_filters.ModelMultipleChoiceFilter(
        field_name="category",
        queryset=Category.objects.all(),
    )
    purpose = django_filters.ModelMultipleChoiceFilter(
        field_name="purpose",
        queryset=Purpose.objects.all(),
    )
    country = django_filters.ModelMultipleChoiceFilter(
        field_name="country",
        queryset=Country.objects.all(),
    )
    wine_type = django_filters.ModelMultipleChoiceFilter(
        field_name="wine_type",
        queryset=WineType.objects.all(),
    )

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
            "wine_type",
        ]
