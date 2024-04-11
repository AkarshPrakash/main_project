from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,HttpResponse
from .models import CustomUser
from django.views.decorators.csrf import csrf_protect
@csrf_protect
# Create your views here.
def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'index.html')
# end def
# myapp/views.py

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.shortcuts import redirect

def loginn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            print("User authenticated:", user.username, user.user_type)
            login(request, user)
            if user.user_type == 'doctor':
                return redirect('doctor_homepage')
            elif user.user_type == 'patient':
                return redirect('patient_homepage')
            else:
                return HttpResponse("Unknown user type")
        else:
            # Handle invalid credentials
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')

        # Create the user
        myuser = CustomUser.objects.create_user(username, email, password, user_type=user_type)

        # Redirect to the login page after successful registration
        return redirect('login')

    return render(request, 'register.html')

