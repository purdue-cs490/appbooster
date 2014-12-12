import os
import shutil

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from appbooster import appconfig
from appbooster import gitmodule
from appbooster import gitolite
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

        try:
            app = Application.objects.create_app(name=appname, user=request.user)
        except IntegrityError as e:
            return render(request, 'error.html', {'error': e.message})

        return redirect('dashboard')


@login_required
def app(request, pk):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    app = get_object_or_404(Application, pk=pk)
    if not hasattr(request.user, 'appuser') or request.user.appuser not in app.appusers.all():
        return render(request, 'error.html', {'error': 'This app is not owned by you'})
    else:
        return render(request, 'application/app.html', {'error': '', 'app': app})


@login_required
def delete(request, pk):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    app = get_object_or_404(Application, pk=pk)
    if not hasattr(request.user, 'appuser') or request.user.appuser not in app.appusers.all():
        return render(request, 'error.html', {'error': 'This app is not owned by you'})

    # Remove nginx config
    if appconfig.remove_nginx_config(app):
        appconfig.reload_nginx()

    # Remove docker
    app_docker = AppDocker()
    if app_docker.exists(app):
        app_docker.stop(app)
        app_docker.remove(app)

    # Remove directories
    appconfig.remove_directoires(app)

    # Remove repo
    gitolite.rm_repo(app.name)
    gitolite.delete_git_folder(app.name)

    app.delete()

    return HttpResponse('OK', status=200)


@csrf_exempt
def deploy_app(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    repo_path = request.POST['repo_path']
    repo_base_path = os.path.basename(repo_path)
    if repo_base_path[-4:] == '.git':
        repo_name = repo_base_path[:-4]
    else:
        repo_name = repo_base_path
    refname = request.POST['refname']
    old_rev = request.POST['old_rev']
    new_rev = request.POST['new_rev']

    app = get_object_or_404(Application, name=repo_name)

    try:
        gitolite.write_ref(repo_path, {'deploy': new_rev})

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
            gitmodule.cloneRepo(app.git_repo_local, app_local_path)

        gitmodule.repoPull(app_local_path, new_rev)

        appconfig.write_uwsgi_config(app)
        appconfig.write_nginx_config(app)
        appconfig.install_virtualenv(app)

        appconfig.reload_nginx()
        app_docker.start(app)

        return HttpResponse('OK', status=200)
    finally:
        gitolite.remove_ref(repo_path, ['deploy'])
