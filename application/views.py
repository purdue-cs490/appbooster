import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from appbooster import appconfig
from appbooster import gitmodule
from appbooster.appdocker import AppDocker
from application.models import Application


class AppDeployException(Exception):
    pass


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'application/create.html', {'error': ''})
    elif request.method == 'POST':
        param = request.POST
        appname = param.get('appname')
        if ' ' in appname:
            return render(request, 'application/create.html', {'error': 'app name cannot contain space'})

        app = Application.objects.create_app(name=appname, user=request.user)
        return redirect('dashboard')


@login_required
def app(request, pk):
    if request.method == 'GET':
        app = Application.objects.get(pk=pk)
        if request.user.appuser not in app.appusers.all():
            return render(request, 'error.html', {'error': 'This app is not owned by you'})
        else:
            return render(request, 'application/app.html', {'error': '', 'app': app})


@csrf_exempt
def deploy_app(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    repo_name = os.path.basename(request.POST.get('repo_path')).rstrip('.git')
    new_rev = request.POST.get('new_rev')
    old_rev = request.POST.get('old_rev')

    app = get_object_or_404(Application, name=repo_name)

    appconfig.init_directories(app)
    app_docker = AppDocker()

    # If container is not created yet
    if not app.container_id:
        container_id = app_docker.create_start(app)
        app.container_id = container_id
        app.save()

    app_docker.stop(app)

    # Update local repo
    app_local_path = app.local_repo_path
    if not os.path.isdir(app_local_path):
        gitmodule.cloneRepo(app.git_repo, app_local_path)
    else:
        gitmodule.repoPull(app_local_path, new_rev)

    appconfig.write_uwsgi_config(app)
    appconfig.write_nginx_config(app)
    appconfig.install_virtualenv(app)

    appconfig.reload_nginx()
    app_docker.start(app)

    return HttpResponse('OK', status=200)
