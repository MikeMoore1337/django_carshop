from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Car, Cart, CartItem, Order


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_data = {
            "brand": "Toyota",
            "model": "Camry",
            "year": 2022,
            "price": 30000.00,
        }
        cls.car = Car.objects.create(**cls.car_data)

    @classmethod
    def tearDownClass(cls):
        cls.car.delete()
        super(CarModelTest, cls).tearDownClass()

    def test_car_creation(self):
        car = Car.objects.get(brand="Toyota", model="Camry", year=2022, price=30000.00)
        self.assertEqual(str(car), "Toyota Camry (2022) - 30000.00")

    def test_car_str_method(self):
        self.assertEqual(str(self.car), "Toyota Camry (2022) - 30000.00")


class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        cls.cart = Cart.objects.create(user=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super(CartModelTest, cls).tearDownClass()

    def test_cart_creation(self):
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.user, self.user)

    def test_cart_items(self):
        car = Car.objects.create(brand="Honda", model="Civic", year=2023, price=25000.00)
        cart_item = CartItem.objects.create(cart=self.cart, car=car, quantity=2)
        self.assertEqual(cart_item.quantity, 2)
        self.assertIn(car, self.cart.items.all())


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        cls.cart = Cart.objects.create(user=cls.user)
        cls.car = Car.objects.create(brand="Ford", model="Mustang", year=2024, price=40000.00)
        cls.cart_item = CartItem.objects.create(cart=cls.cart, car=cls.car, quantity=3)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super(OrderModelTest, cls).tearDownClass()

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=self.cart_item.car.price * self.cart_item.quantity,
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, self.cart_item.car.price * self.cart_item.quantity)

    def test_add_items_to_order(self):
        order = Order.objects.create(user=self.user, total_price=0)
        order.add_items_to_order(cart_items=[self.cart_item])
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertEqual(order.orderitem_set.first().car, self.cart_item.car)
        self.assertEqual(order.orderitem_set.first().quantity, self.cart_item.quantity)
