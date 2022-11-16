from django.urls import path
from hello import views
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic.base import RedirectView


urlpatterns = [
    path("", views.stock, name="stock"),
    path("contact/", views.contact, name="contact"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
]