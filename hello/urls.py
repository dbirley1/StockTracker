from django.urls import path
from hello import views
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic.base import RedirectView


urlpatterns = [
    path("", views.stock, name="stock"),
    path("login", views.user_login, name="login"),
    path("register", views.register, name="register"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('logout', views.user_logout, name="logout")
]