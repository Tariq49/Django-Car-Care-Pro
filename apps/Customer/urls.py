from django.urls import path
from . import views

app_name = 'customer-urls'
urlpatterns = [


    path('',views.list_customers, name='customers'),
    path('<int:id>', views.get_customer, name='get-customer'),
    path('create/', views.create_customer, name='create-customer'),
    path('<int:id>/update', views.update_customer, name='update-customer'),
    path('<int:id>/delete', views.delete_customer, name='delete-customer'),
    
    path('service/requests/', views.list_service_requests, name='list-service-requests'),
    path('service/requests/<int:id>', views.get_service_request, name='service-request-detail'),
    path('service/requests/create/', views.create_service_requests, name='create-service-requests'),  
    path('service/requests/<int:id>/update/', views.update_service_request, name='update_service_request'),
    path('service/requests/<int:id>/delete/', views.delete_service_request, name='delete_service_request'),

]



