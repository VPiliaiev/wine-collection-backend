from django.contrib import admin

from cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("wine", "quantity")
    can_delete = False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "total_items_count")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "id")
    inlines = [CartItemInline]

    def total_items_count(self, obj):
        return obj.items.count()

    total_items_count.short_description = "quantity product"
