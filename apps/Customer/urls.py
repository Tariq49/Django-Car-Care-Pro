from django.urls import path
from . import views

app_name = 'customer-urls'
urlpatterns = [


    path('', views.customer_list_create, name='customer_list_create'),
    path('detail/', views.customer_detail, name='customer_detail'),
    
    path('service/request/', views.list_service_requests, name='list_service_requests'), 
    path('service/request/<int:id>/', views.service_request_detail, name='service_request_detail'),  

    path('feedback/', views.feedback_list_or_create, name='feedback-list-or-create'),
    path('feedback/<int:id>/', views.feedback_detail, name='feedback-detail'),

   

]

 

