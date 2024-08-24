from django.urls import path
from . import views

app_name = 'customer-urls'
urlpatterns = [
    path('',views.list_customers, name='list-customers'),
    path('<int:id>/', views.get_customer, name='get-customer'),
    path('create/', views.create_customer, name='create-customer'),
    path('update/<int:id>/', views.update_customer, name='update-customer'),
    path('delete/<int:id>/', views.delete_customer, name='delete-customer'),
]



