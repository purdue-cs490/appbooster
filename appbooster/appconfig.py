import grp
import os
import shutil

from django.conf import settings
from django.template import loader

NGINX_CONFIG_DIR = '/etc/nginx/sites-enabled'
APPDCN_GID = grp.getgrnam('appdcn').gr_gid


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def init_directories(app_name):
    control_path = os.path.join(settings.HOST_CONTROL_DIR, app_name)
    app_path = os.path.join(settings.HOST_APP_DIR, app_name)

    if not os.path.isdir(control_path):
        os.mkdir(control_path)

    if not os.path.isdir(app_path):
        os.mkdir(app_path)

    os.chown(control_path, -1, APPDCN_GID)
    os.chown(app_path, -1, APPDCN_GID)


def write_nginx_config(app_name):
    socket_name = app_name + '.socket'
    nginx_access_name = app_name + '_nginx_access'
    nginx_error_name = app_name + '_nginx_error'

    control_path = os.path.join(settings.HOST_CONTROL_DIR, app_name)
    app_path = os.path.join(settings.HOST_APP_DIR, app_name)
    nginx_config_path = os.path.join(NGINX_CONFIG_DIR, app_name)

    nginx_access_path = os.path.join(app_path, nginx_access_name)
    nginx_error_path = os.path.join(app_path, nginx_error_name)

    init_directories(app_name)

    touch(nginx_access_path)
    os.chown(nginx_access_path, -1, APPDCN_GID)
    touch(nginx_error_path)
    os.chown(nginx_error_path, -1, APPDCN_GID)

    config = {
        'uwsgi_pass': 'unix://%s' % os.path.join(control_path, socket_name),
        'access_log': nginx_access_path,
        'error_log': nginx_error_path,
    }

    nginx_config = loader.render_to_string('nginx_config', config)

    with open(nginx_config_path, 'w+') as nginx_config_file:
        if nginx_config_file.read() != nginx_config:
            nginx_config_file.write(nginx_config)


def write_uwsgi_config(app_name):
    socket_name = app_name + '.socket'
    virtualenv_name = app_name + '.virtualenv'
    log_name = app_name + '_uwsgi.log'
    uwsgi_config_name = app_name + '.ini'

    app_socket_path = os.path.join(settings.CONTAINER_CONTROL_DIR, socket_name)
    app_chdir_path = os.path.join(settings.CONTAINER_APP_DIR, app_name)
    app_virtualenv_path = os.path.join(settings.CONTAINER_APP_DIR, virtualenv_name)
    app_log_path = os.path.join(settings.CONTAINER_APP_DIR, log_name)

    control_path = os.path.join(settings.HOST_CONTROL_DIR, app_name)
    uwsgi_config_path = os.path.join(control_path, uwsgi_config_name)

    init_directories(app_name)

    config = {
        'socket': app_socket_path,
        'chdir': app_chdir_path,
        'virtualenv': app_virtualenv_path,
        'logto': app_log_path,
    }

    uwsgi_config = loader.render_to_string('uwsgi_config', config)

    with open(uwsgi_config_path, 'w+') as uwsgi_config_file:
        if uwsgi_config_file.read() != uwsgi_config:
            uwsgi_config_file.write(uwsgi_config)

    touch(uwsgi_config_path)


def remove_nginx_config(app_name):
    nginx_config_path = os.path.join(NGINX_CONFIG_DIR, app_name)

    if os.path.exists(nginx_config_path):
        os.remove(nginx_config_path)


def remove_uwsgi_config(app_name):
    control_path = os.path.join(settings.HOST_CONTROL_DIR, app_name)
    app_path = os.path.join(settings.HOST_APP_DIR, app_name)

    if os.path.isdir(control_path):
        shutil.rmtree(control_path)

    if os.path.isdir(app_path):
        shutil.rmtree(app_path)


if __name__ == '__main__':
    write_nginx_config('appbooster-test')
    write_uwsgi_config('appbooster-test')
