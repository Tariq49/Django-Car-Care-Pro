from django.urls import path
from . import views

app_name = 'customer-urls'
urlpatterns = [


    path('',views.list_customers, name='customers'),
    path('<int:id>', views.get_customer, name='get-customer'),
    path('create/', views.create_customer, name='create-customer'),
    path('<int:id>/update', views.update_customer, name='update-customer'),
    path('<int:id>/delete', views.delete_customer, name='delete-customer'),
    
    path('service/request/', views.list_service_requests, name='list_service_requests'), 
    path('service/request/<int:id>/', views.service_request_detail, name='service_request_detail'),  

    path('feedback/', views.feedback_list_or_create, name='feedback-list-or-create'),
    path('feedback/<int:id>/', views.feedback_detail, name='feedback-detail'),



]



