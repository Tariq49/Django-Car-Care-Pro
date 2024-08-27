from django.urls import path
from . import views 
from .views.mechanic import MechanicDetailView, MechanicListCreateView


app_name = 'mechanic-urls'

urlpatterns = [

<<<<<<< HEAD
    path('', views.mechanic_list_create, name='mechanic_list_create'),
    path('<int:id>/', views.mechanic_detail, name='mechanic_detail'),
    path('mechanic-price-per-service/', views.mechanic_price_per_service_list, name='mechanic-price-per-service-list'),
    path('mechanic-price-per-service/<int:pk>/', views.mechanic_price_per_service_detail, name='mechanic-price-per-service-detail')
]  
=======
    path('', MechanicListCreateView.as_view(), name='mechanic-list-create'),
    path('<int:pk>/', MechanicDetailView.as_view(), name='mechanic-detail'),
]
>>>>>>> d87822f (added user)
