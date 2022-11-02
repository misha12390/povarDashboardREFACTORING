from django.contrib import admin
from django.urls import path, include
from allauth.account import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bar/', include('bar.urls')),
    path("login/", account_views.login, name="account_login"),
]
