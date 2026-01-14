from rest_framework import serializers
from cart.models import Cart, CartItem


class CartItemListSerializer(serializers.ModelSerializer):
    wine_id = serializers.IntegerField(source="wine.id", read_only=True)
    wine_name = serializers.CharField(source="wine.name", read_only=True)
    wine_price = serializers.DecimalField(
        source="wine.price", max_digits=10, decimal_places=2, read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            "id",
            "wine_id",
            "wine_name",
            "wine_price",
            "quantity",
            "subtotal",
        )

    def get_subtotal(self, obj):
        return obj.wine.price * obj.quantity


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("wine", "quantity")

    def validate(self, data):
        wine = data["wine"]
        quantity = data["quantity"]
        if wine.stock < quantity:
            raise serializers.ValidationError(f"Only {wine.stock} wines available")
        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemListSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            "id",
            "status",
            "items",
            "total_price",
            "created_at",
            "updated_at",
        )

    def get_total_price(self, obj):
        return sum(item.wine.price * item.quantity for item in obj.items.all())
