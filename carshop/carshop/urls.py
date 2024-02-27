from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import home, registration, login, logout

urlpatterns = [
    path("", home, name="home"),
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path("admin/", admin.site.urls, name="admin"),
    path("cars/", include("cars.urls")),

]

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )
