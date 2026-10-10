from django.contrib import admin
from .models import Product, Sale
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "stock_on_hand", "reorder_level", "lead_time_days")
    search_fields = ("sku", "name", "category")
    list_filter = ("category",)
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("product", "date", "quantity", "unit_price")
    list_filter = ("date",)
