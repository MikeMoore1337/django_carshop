from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import home, registration

urlpatterns = [
    path("", home, name="home"),
    path('registration/', registration, name='registration'),
    path("admin/", admin.site.urls, name="admin"),
    path("cars/", include("cars.urls")),

]

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )
