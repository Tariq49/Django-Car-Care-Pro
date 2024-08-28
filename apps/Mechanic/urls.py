from django.urls import path
from . import views 
from .views.mechanic import MechanicDetailView, MechanicListCreateView


app_name = 'mechanic-urls'

urlpatterns = [

    path('price/', views.mechanic_price_per_service_list, name='mechanic-price-per-service-list'),
    path('price/<int:pk>/', views.mechanic_price_per_service_detail, name='mechanic-price-per-service-detail'),
    path('', MechanicListCreateView.as_view(), name='mechanic-list-create'),
    path('<int:pk>/', MechanicDetailView.as_view(), name='mechanic-detail'),
]
