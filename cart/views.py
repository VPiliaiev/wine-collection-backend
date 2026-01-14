from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.GenericViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.prefetch_related("items__wine")

    def get_current_cart(self):
        if self.request.user.is_authenticated:
            return (
                self.get_queryset()
                .filter(user=self.request.user, status=Cart.StatusChoices.ACTIVE)
                .first()
            )

        cart_id = self.request.query_params.get("cart_id") or self.request.data.get(
            "cart_id"
        )
        if cart_id:
            return (
                self.get_queryset()
                .filter(id=cart_id, status=Cart.StatusChoices.ACTIVE)
                .first()
            )
        return None

    def get_or_create_current_cart(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(
                user=self.request.user, status=Cart.StatusChoices.ACTIVE
            )
            return cart

        cart_id = self.request.query_params.get("cart_id") or self.request.data.get(
            "cart_id"
        )
        if cart_id:
            cart = Cart.objects.filter(
                id=cart_id, status=Cart.StatusChoices.ACTIVE
            ).first()
            if cart:
                return cart

        return Cart.objects.create(status=Cart.StatusChoices.ACTIVE)

    @extend_schema(
        summary="Retrieve current cart",
        parameters=[
            OpenApiParameter(
                "cart_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description="Cart UUID from localStorage",
            )
        ],
    )
    def list(self, request):
        cart = self.get_current_cart()
        if not cart:
            return Response({"id": None, "items": [], "total_price": 0})
        return Response(self.get_serializer(cart).data)

    @extend_schema(
        summary="Add item to cart",
        description="Create a new cart if cart_id is not provide",
        parameters=[
            OpenApiParameter(
                "cart_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description="Existing cart UUID",
            )
        ],
        request=CartItemSerializer,
    )
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self.get_or_create_current_cart()
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wine = serializer.validated_data["wine"]
        quantity = serializer.validated_data["quantity"]

        with transaction.atomic():
            existing_item = cart.items.filter(wine=wine).first()
            current_in_cart = existing_item.quantity if existing_item else 0

            if current_in_cart + quantity > wine.stock:
                return Response(
                    {
                        "error": f"Cannot add more. Stock: {wine.stock}, in your cart: {current_in_cart}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cart_item, created = CartItem.objects.select_for_update().get_or_create(
                cart=cart, wine=wine, defaults={"quantity": quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        cart.refresh_from_db()
        return Response(self.get_serializer(cart).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update item quantity",
        description="Updates quantity to a specific value. If quantity is 0, item is removed",
        parameters=[
            OpenApiParameter(
                "cart_id", OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True
            ),
            OpenApiParameter("wine_id", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("quantity", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        request=CartItemSerializer,
    )
    @action(detail=False, methods=["patch"])
    def update_quantity(self, request):
        cart = self.get_current_cart()
        if not cart:
            return Response({"error": "Cart not found"}, status=404)

        wine_id = request.data.get("wine_id") or request.query_params.get("wine_id")
        quantity_raw = request.data.get("quantity") or request.query_params.get(
            "quantity"
        )

        if wine_id is None or quantity_raw is None:
            return Response({"error": "wine_id and quantity are required"}, status=400)

        try:
            quantity = int(quantity_raw)
        except (ValueError, TypeError):
            return Response({"error": "Quantity must be a number"}, status=400)

        with transaction.atomic():
            try:
                item = (
                    cart.items.select_for_update()
                    .select_related("wine")
                    .get(wine_id=wine_id)
                )

                if quantity > item.wine.stock:
                    return Response(
                        {
                            "error": f"Only {item.wine.stock} bottles available in stock."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if quantity > 0:
                    item.quantity = quantity
                    item.save()
                else:
                    item.delete()
            except CartItem.DoesNotExist:
                return Response({"error": "Wine not found in cart"}, status=404)

        cart.refresh_from_db()
        return Response(self.get_serializer(cart).data)

    @extend_schema(
        summary="Decrease quantity by 1",
        description="Decrease quantity. Remove item if quantity equal 0",
        parameters=[
            OpenApiParameter(
                "cart_id", OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True
            ),
            OpenApiParameter(
                "wine_id", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True
            ),
        ],
    )
    @action(detail=False, methods=["delete"], url_path="remove-one")
    def remove_one(self, request):
        cart = self.get_current_cart()
        if not cart:
            return Response({"error": "Cart not found"}, status=404)

        wine_id = request.query_params.get("wine_id") or request.data.get("wine_id")
        if not wine_id:
            return Response(
                {"error": "wine_id is required as query parameter"}, status=400
            )

        with transaction.atomic():
            try:
                item = cart.items.select_for_update().get(wine_id=wine_id)
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                else:
                    item.delete()
            except CartItem.DoesNotExist:
                return Response({"error": "Wine not found in cart"}, status=404)
        cart.refresh_from_db()
        return Response(self.get_serializer(cart).data)

    @extend_schema(
        summary="Clear all items from cart",
        description="Removes all items but keeps the cart object active",
        parameters=[
            OpenApiParameter(
                "cart_id", OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True
            ),
        ],
    )
    @action(detail=False, methods=["delete"])
    def clear(self, request):
        cart = self.get_current_cart()

        if not cart:
            return Response({"id": None, "items": [], "total_price": 0})

        with transaction.atomic():
            cart.items.all().delete()

        cart.refresh_from_db()
        return Response(self.get_serializer(cart).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Merge anonymous cart to user",
        description="Transfers all items from anonymous cart to the authenticated user cart",
        parameters=[
            OpenApiParameter(
                "cart_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                required=True,
                description="Anonymous cart UUID",
            ),
        ],
    )
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def merge_unauthorized_cart_to_user(self, request):
        anonymous_cart_id = self.request.query_params.get(
            "cart_id"
        ) or request.data.get("cart_id")
        if not anonymous_cart_id:
            return Response({"error": "cart_id is required"}, status=400)

        with transaction.atomic():
            anon_cart = Cart.objects.filter(
                id=anonymous_cart_id, user=None, status=Cart.StatusChoices.ACTIVE
            ).first()

            if not anon_cart:
                return Response({"error": "Anonymous cart not found"}, status=404)

            user_cart, _ = Cart.objects.get_or_create(
                user=request.user, status=Cart.StatusChoices.ACTIVE
            )

            anon_items = anon_cart.items.select_for_update().all()
            for item in anon_items:
                user_item, created = CartItem.objects.get_or_create(
                    cart=user_cart, wine=item.wine, defaults={"quantity": item.quantity}
                )
                if not created:
                    user_item.quantity += item.quantity
                    user_item.save()

            anon_cart.delete()

        user_cart.refresh_from_db()
        return Response(self.get_serializer(user_cart).data)
