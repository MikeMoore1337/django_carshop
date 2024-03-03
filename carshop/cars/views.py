from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages_constants
from django.contrib.messages import get_messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Car, Cart, CartItem, Order


class CarListView(ListView):
    model = Car
    template_name = "cars/catalog.html"
    context_object_name = "cars"


class CarDetailView(DetailView):
    model = Car
    template_name = "cars/car_detail.html"
    context_object_name = "car"


@login_required
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


class ConfirmOrderView(TemplateView):
    template_name = "cars/confirm_order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart_items = CartItem.objects.filter(cart__user=user)
        total_price = sum(item.car.price * item.quantity for item in cart_items)
        context['cart_items'] = cart_items
        context['total_price'] = total_price

        # Удаление уведомления после использования
        if 'order_placed' in self.request.session:
            del self.request.session['order_placed']

        return context


@login_required
def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.car.price * item.quantity for item in cart_items)

    if request.method == 'POST' and 'buy_button' in request.POST:
        if not cart_items.exists():
            messages.error(request, "Your cart is empty. Add items to your cart before proceeding.")
            return redirect('view_cart')

        try:
            latest_order = Order.objects.filter(user=user).latest('created_at')
        except Order.DoesNotExist:
            latest_order = None

        if latest_order is None:
            with transaction.atomic():
                latest_order = Order.objects.create(total_price=total_price, user=user)
                latest_order.add_items_to_order(cart_items)
                cart_items.delete()

            messages.success(request, "Order placed successfully. Your order will be processed.")

            messages.set_level(request, messages_constants.SUCCESS)
            messages.success(request, "Order placed successfully. Your order will be processed.")

            return redirect('confirm_order')

    context = {'cart_items': cart_items, 'total_price': total_price, 'order_placed': False}
    storage = get_messages(request)
    storage.used = True

    return render(request, 'cars/cart.html', context)


def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    added_to_cart = request.GET.get('added_to_cart', False)
    return render(request, 'cars/car_detail.html', {'car': car, 'added_to_cart': added_to_cart})


def remove_from_cart(request, car_id):
    cart_item = get_object_or_404(CartItem, car__pk=car_id)
    cart_item.delete()
    messages.success(request, "Car removed from your cart.")
    return redirect('view_cart')


@login_required
def confirm_order(request):
    return render(request, 'cars/confirm_order.html')
