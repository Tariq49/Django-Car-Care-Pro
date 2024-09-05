from django.urls import path
from . import views 
from .views.mechanic import  MechanicListCreateView


app_name = 'mechanic-urls'

urlpatterns = [

    path('', MechanicListCreateView.as_view(), name='mechanic-list-create'),
   # path('<int:pk>/', MechanicDetailView.as_view(), name='mechanic-detail'),

    path('price/', views.mechanic_price_per_service_list, name='mechanic-price-per-service-list'),
     
  
    path('requests/', views.mechanic_service_requests, name='mechanic_service_requests'),
    path('requests/<int:pk>/', views.update_service_request, name='update_service_request'),
   
]
