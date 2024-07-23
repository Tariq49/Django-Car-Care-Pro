from django.urls import path
from .views import customer_home,delete_account,SignUpView

urlpatterns = [
    path('customer/', customer_home, name='customer_home'),
    path('delete-account/', delete_account, name='delete_account'),
    path('signup/', SignUpView, name='signup'),
]