from django.urls import path
from .views import home_view,about_us,website,logout_view

urlpatterns = [
    path('', home_view, name='home'), 
    path('website/', website, name='website'),
    path('about/', about_us, name='about_us'),
    path('logout/', logout_view, name='logout'),
]
