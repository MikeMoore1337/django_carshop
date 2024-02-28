from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .models import Car, Cart, CartItem, Order, OrderItem


class CarListView(ListView):
    model = Car
    template_name = "cars/catalog.html"
    context_object_name = "cars"


class CarDetailView(DetailView):
    model = Car
    template_name = "cars/car_detail.html"
    context_object_name = "car"


def add_to_cart(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(car=car, cart=cart)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    messages.success(request, f"{car.brand} {car.model} added to your cart.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'quantity': cart_item.quantity})

    return redirect('view_cart')


@login_required
def view_cart(request):
    user = request.user

    # Получить или создать корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.car.price * item.quantity for item in cart_items)

    # Попытка получить существующий заказ или создать новый
    try:
        order = Order.objects.get(user=user)
    except Order.DoesNotExist:
        order = None

    if request.method == 'POST' and 'buy_button' in request.POST:
        if order is None:
            # Если заказ не существует, создаем новый
            order = Order.objects.create(total_price=total_price, user=user)
        else:
            # Если заказ существует, обновляем его
            order.total_price = total_price
            order.save()

        # Добавление элементов заказа
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, car=cart_item.car, quantity=cart_item.quantity)

        # Очистка корзины после успешного заказа
        cart_items.delete()
        messages.success(request, "Order placed successfully.")

    return render(request, 'cars/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    added_to_cart = request.GET.get('added_to_cart', False)
    return render(request, 'cars/car_detail.html', {'car': car, 'added_to_cart': added_to_cart})


def remove_from_cart(request, car_id):
    cart_item = get_object_or_404(CartItem, car__pk=car_id)
    cart_item.delete()
    messages.success(request, "Car removed from your cart.")
    return redirect('view_cart')
