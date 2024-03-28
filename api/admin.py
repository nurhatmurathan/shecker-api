from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "price")
    list_display_links = ('id', "name")


class FridgeProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'fridge_link', "product_link", "quantity")
    list_display_links = ('id',)

    def fridge_link(self, obj):
        url = reverse("admin:api_fridge_change", args=[obj.fridge.account])
        return format_html('<a href="{}">{}</a>', url, obj.fridge)

    fridge_link.short_description = 'Fridge'

    def product_link(self, obj):
        url = reverse("admin:api_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product)

    product_link.short_description = 'product'


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'fridge_product_link', "order_link", "amount")
    list_display_links = ('id',)

    def fridge_product_link(self, obj):
        url = reverse("admin:api_fridgeproduct_change", args=[obj.fridge_product.id])
        return format_html('<a href="{}">{}</a>', url, obj.fridge_product)

    fridge_product_link.short_description = 'Fridge product'

    def order_link(self, obj):
        url = reverse("admin:api_order_change", args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order)

    order_link.short_description = 'Order'


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', "order_link", "check_txn_id", "pay_txn_id", "txn_date")
    list_display_links = ('id',)

    def order_link(self, obj):
        url = reverse("admin:api_order_change", args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order)

    order_link.short_description = 'Order'


admin.site.register(Fridge)
admin.site.register(Product, ProductAdmin)
admin.site.register(FridgeProduct, FridgeProductAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
