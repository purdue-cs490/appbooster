from django.shortcuts import render, redirect
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'index.html')

def logout(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'index.html')

def not_completed(request):
    return render(request, 'index.html')
