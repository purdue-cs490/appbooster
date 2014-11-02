import os

from django.template import loader

CONTROL_DIR = '/u/controls'
APP_DIR = '/u/apps'
APP_CONTROL_DIR = '/u/control'
APP_APP_DIR = '/u/app'
NGINX_CONFIG_DIR = '/etc/nginx/site-enabled'


def write_nginx_config(app_name):
    socket_name = app_name + '.socket'
    nginx_access_name = app_name + '_nginx_access'
    nginx_error_name = app_name + '_nginx_error'

    control_path = os.path.join(CONTROL_DIR, app_name)
    app_path = os.path.join(APP_DIR, app_name)
    nginx_config_path = os.path.join(NGINX_CONFIG_DIR, app_name)

    if not os.path.isdir(control_path):
        os.mkdir(control_path)
        os.chown(control_path, -1, 'appdcn')

    if not os.path.isdir(app_path):
        os.mkdir(app_path)
        os.chown(app_path, -1, 'appdcn')

    config = {
        'uwsgi_pass': 'unix://%s' % os.path.join(control_path, socket_name),
        'access_log': os.path.join(app_path, nginx_access_name),
        'error_log': os.path.join(app_path, nginx_error_name),
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

    app_socket_path = os.path.join(APP_CONTROL_DIR, socket_name)
    app_chdir_path = os.path.join(APP_APP_DIR, app_name)
    app_virtualenv_path = os.path.join(APP_APP_DIR, virtualenv_name)
    app_log_path = os.path.join(APP_APP_DIR, log_name)

    control_path = os.path.join(CONTROL_DIR, app_name)
    app_path = os.path.join(APP_DIR, app_name)
    uwsgi_config_path = os.path.join(control_path, uwsgi_config_name)

    if not os.path.isdir(control_path):
        os.mkdir(control_path)
        os.chown(control_path, -1, 'appdcn')

    if not os.path.isdir(app_path):
        os.mkdir(app_path)
        os.chown(app_path, -1, 'appdcn')

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


if __name__ == '__main__':
    write_nginx_config('appbooster-test')
    write_uwsgi_config('appbooster-test')
