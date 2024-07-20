from django.urls import path
from .views import home_view,signup_view,login_view,about_us,website

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('website/', website, name='website'),
    path('about/', about_us, name='about_us'),
]
