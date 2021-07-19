from django.contrib.messages.api import error
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, "registration.html")

def create(request):
    errors = User.objects.basic_validator(request.POST)
    
    user = User.objects.filter(email=request.POST['email'])
    if user:
        messages.error(request, "Email already exists.")
        return redirect('/')
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    user1= User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw
    )
    request.session['log_user_id'] = user1.id
    return redirect('/dash')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['log_user_id'] = logged_user.id
            return redirect('/dash')
    else:
            messages.error(request, 'Invalid email or password')
    messages.error(request, "Email does not exist")
    return redirect('/')

def dash(request):
    context = {
        'user' : User.objects.get(id=request.session['log_user_id'])
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect("/")
