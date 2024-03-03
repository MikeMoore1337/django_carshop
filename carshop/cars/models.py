from django.contrib.auth.models import User
from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.price:.2f}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField("Car", through="CartItem")

    objects = models.Manager()


class CartItem(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    objects = models.Manager()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def add_items_to_order(self, cart_items):
        for cart_item in cart_items:
            OrderItem.objects.create(order=self, car=cart_item.car, quantity=cart_item.quantity)


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    car = models.ForeignKey("Car", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    objects = models.Manager()
