from django.urls import path
from . import views

app_name = 'mechanic-urls'

urlpatterns = [

    path('', views.mechanic_list_create, name='mechanic_list_create'),
    path('<int:id>/', views.mechanic_detail, name='mechanic_detail'),
]