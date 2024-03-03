# Register your models here.
# admin / admin

from django.contrib import admin

from .models import Car, Order, OrderItem

admin.site.register(Car)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)
