from django.conf import settings

from docker import Client

CONTAINER_IMAGE = 'appbooster-container'
CONTAINER_NAME_PREFIX = 'APPD_'

STOP_TIMEOUT = 20   # 20 secs


class AppDockerException(Exception):
    pass


class AppDocker(object):

    def __init__(self):
        self.client = Client()

    def create_start(self, app):
        app_name = app.name
        container_name = CONTAINER_NAME_PREFIX + app_name

        create_args = {
            'image': CONTAINER_IMAGE,
            'tty': False,
            'detach': True,
            'mem_limit': settings.CONTAINER_MEM_LIMIT,
            'name': container_name,
        }

        container = self.client.create_container(**create_args)
        container_id = container.get('Id')

        if not container_id:
            raise AppDockerException("Failed to create container")

        host_control_path = app.host_control_path()
        host_app_path = app.host_app_path()

        bind_volumes = {
            host_control_path: {
                'bind': settings.CONTAINER_CONTROL_DIR,
                'ro': False,
            },
            host_app_path: {
                'bind': settings.CONTAINER_APP_DIR,
                'ro': False,
            },
        }

        start_args = {
            'container': container_id,
            'binds': bind_volumes,
        }

        self.client.start(**start_args)

        return container_id

    def stop(self, app):
        container_id = app.container_id
        stop_args = {
            'container': container_id,
            'timeout': STOP_TIMEOUT,
        }

        self.client.stop(**stop_args)

    def start(self, app):
        container_id = app.container_id
        start_args = {
            'container': container_id,
        }

        self.client.start(**start_args)
