# apps/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import logout


def home_view(request):
    return render(request, 'home.html')



def about_us(request):
    return render(request, 'about_us.html')

def website(request):
    return render(request, 'website.html')

def logout_view(request):
    logout(request)  
    return redirect('home') 