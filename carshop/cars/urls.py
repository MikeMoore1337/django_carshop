from django.urls import path

from .views import CarDetailView, CarListView, add_to_cart, confirm_order, remove_from_cart, view_cart

urlpatterns = [
    path("catalog.html", CarListView.as_view(), name="catalog"),
    path("car_detail/<int:pk>/", CarDetailView.as_view(), name="car_detail"),
    path("add_to_cart/<int:car_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", view_cart, name="view_cart"),
    path('cart/', view_cart, name='cart'),
    path('remove_from_cart/<int:car_id>/', remove_from_cart, name='remove_from_cart'),
    path('confirm_order/', confirm_order, name='confirm_order'),
]
