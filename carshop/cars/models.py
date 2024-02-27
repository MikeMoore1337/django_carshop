from django.contrib.auth.models import User as DjangoUser
from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.price:.2f}"


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)


class Cart(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    items = models.ManyToManyField('Car', through='CartItem')

    objects = models.Manager()


class CartItem(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    objects = models.Manager()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Car', through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class OrderItem(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    objects = models.Manager()
