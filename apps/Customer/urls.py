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

    path('feedbacks/', views.customer_feedback_list, name='customer-feedback-list'),
    path('feedback/create/', views.customer_feedback_create, name='customer-feedback-create'),
    path('feedback/<int:id>/', views.customer_feedback_detail, name='customer-feedback-detail'),
    path('feedback/<int:id>/update/', views.customer_feedback_update, name='customer-feedback-update'),
    path('feedback/<int:id>/delete/', views.customer_feedback_delete, name='customer-feedback-delete'),



]



