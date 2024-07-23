from django.urls import path
from .views import mechanic_home,delete_account

urlpatterns = [
    path('mechanic/', mechanic_home, name='mechanic_home'),
    path('delete-account/', delete_account, name='delete_account'),
]