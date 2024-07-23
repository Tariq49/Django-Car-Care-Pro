from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.utils import timezone
from django.db import IntegrityError

User = get_user_model

def customer_home(request):
    return render(request, 'customer_home.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home') 
    return render(request, 'confirm_delete.html')

def SignUpView(request):


    if request.method == 'POST':
        # Extract data from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')
        profile_image = request.FILES.get('profile_image')

        

        # Validate gender
        if gender not in ['M', 'F']:
            return render(request, 'customer_home.html', {'error': 'Invalid gender value. Choose "M" for Male or "F" for Female.'})

        if not contact_number.isdigit() or len(contact_number) != 9:
           
            return render(request, 'customer_home.html', {'error': 'Contact number should be 9 digits.'})
        
        try:
            # Create a new customer instance
            customer = Customer(
                username=username,
                first_name=first_name,
                last_name=last_name,
                address=address,
                email=email,
                gender=gender,
                contact_number=contact_number,
                profile_image=profile_image,
                date_of_join=timezone.now()  
            )

            # Set password using set_password method
            customer.set_password(password)
            customer.save()

            # Log the user in
            login(request, customer)
            messages.success(request, 'Sign up successful!')
            return redirect('home')
        
        except IntegrityError as e:
            # Handle IntegrityError, e.g., if email or username already exists
            error_message = 'A user with this email or username already exists.'
            messages.success(request, error_message)
            return render(request, 'customer_home.html', {'error': error_message})

    
    return render(request, 'customer_home.html')     