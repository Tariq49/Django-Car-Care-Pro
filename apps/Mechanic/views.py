from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def mechanic_home(request):
    return render(request, 'mechanic_home.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home') 
    return render(request, 'confirmm_delete.html')