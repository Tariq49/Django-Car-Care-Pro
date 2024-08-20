from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout,authenticate
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
            messages.error(request, 'Contact number should be 9 digits')
           
            return redirect("customer_home")
        
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
            logout(request)
            messages.success(request, 'Sign up successful!')
            return redirect('home')
        
        except IntegrityError as e:
            # Handle IntegrityError, e.g., if email or username already exists
            error_message = 'A user with this email or username already exists.'
            messages.error(request, error_message)
            return redirect("customer_home")

    
    return render(request, 'customer_home.html')     

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to home or any other page
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'customer_home.html')

    return render(request, 'customer_home.html')
