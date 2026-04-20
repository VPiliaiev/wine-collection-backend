from rest_framework import serializers

from wine.models import Wine, WineType, Category, Mood, Country, Purpose


class WineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineType
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ("id", "name")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class WineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = (
            "id",
            "name",
            "volume",
            "price",
            "image"
        )


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = ("id", "name")


class WineRetrieveSerializer(serializers.ModelSerializer):
    moods = MoodSerializer(many=True, read_only=True)
    country = CountrySerializer(many=False, read_only=True)
    wine_type = WineTypeSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    image = serializers.ImageField(read_only=True)
    in_stock = serializers.ReadOnlyField()
    purpose = PurposeSerializer(many=False, read_only=True)

    class Meta:
        model = Wine
        fields = (
            "id",
            "name",
            "volume",
            "price",
            "description",
            "country",
            "wine_type",
            "category",
            "moods",
            "created_at",
            "image",
            "stock",
            "in_stock",
            "purpose"
        )
        read_only_fields = ("id", "created_at", "stock", "in_stock")
