from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def contact(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'GET':
        context = {
            'next': request.GET.get('next'),
            'error': '',
        }
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        param = request.POST
        username = param.get('username')
        password = param.get('password')
        next_ = param.get('next')
        user = authenticate(username=username, password=password)
        if user is not None:
            _login(request, user)
            if next_ != 'None' and next_:
                respond = redirect(next_)
            else:
                respond = redirect('dashboard')
        else:
            return render(
                request, 'login.html',
                {'error': 'Incorrect login'}
            )
        return respond


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'error': ''})
    elif request.method == 'POST':
        param = request.POST
        username = param.get('email')
        firstname = param.get('firstname')
        lastname = param.get('lastname')
        email = param.get('email')
        password = param.get('password')
        repassword = param.get('repassword')
        if not username or not firstname or not lastname:
            return render(request, 'register.html', {'error': 'Please fill out all required fields'})
        if not email:
            return render(request, 'register.html', {'error': 'Please fill out address'})
        if repassword != password:
            return render(request, 'register.html', {'error': 'Password not same'})
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'register.html', {'error': 'Please use correct email'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username Exists'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email Exists'})
        else:
            user = User.objects.create_user(
                username,
                email,
                password,
                first_name=firstname,
                last_name=lastname,
            )
            user = authenticate(username=username, password=password)
            _login(request, user)
            respond = redirect('dashboard')
            return respond
    else:
        return render(request, 'register.html', {'error': ''})


@login_required
def logout(request):
    _logout(request)
    return redirect('index')


def profile(request):
    return render(request, 'index.html')


def not_completed(request):
    return render(request, 'index.html')
