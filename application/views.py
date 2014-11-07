from django.shortcuts import render, redirect
from application.models import Application

# Create your views here.
def create(request):
    if request.method == 'GET':
        return render(request, 'application/create.html', {'error': ''})
    elif request.method == 'POST':
        param = request.POST
        appname = param.get('appname')
        app = Application.objects.create_app(name=appname, user=request.user)
        return redirect('dashboard')