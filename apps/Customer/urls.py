from django.urls import path
from .views import customer_home

urlpatterns = [
    path('customer/', customer_home, name='customer_home'),
   
]