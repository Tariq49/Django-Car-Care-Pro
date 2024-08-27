from django.urls import path
from . import views


app_name = 'user-urls'
urlpatterns = [
    path('', views.user_list_create, name='user-list_create'),
    path('<int:pk>/', views.user_detail, name='user-detail'),
]
