from django.shortcuts import render, redirect
from django.contrib.auth import login
from apps.accounts.forms import SignUpForm, LoginForm

def home_view(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = SignUpForm(request.POST)
            login_form = LoginForm()
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('home')
        elif 'login' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            signup_form = SignUpForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')
    else:
        signup_form = SignUpForm()
        login_form = LoginForm()

    return render(request, 'home.html', {
        'signup_form': signup_form,
        'login_form': login_form
    })
