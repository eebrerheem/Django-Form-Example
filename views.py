from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
    
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})




def login(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        
        else:
            messages.info(request,'Please check username and password')
            return redirect('login')
    
    else:    
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
        
        
@login_required(login_url='/account/login')    
def profile(request):
    
    return render(request, 'profile.html')