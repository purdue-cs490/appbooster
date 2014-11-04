import os

from django.conf import settings

from docker import Client

CONTAINER_IMAGE = 'appbooster-container'
CONTAINER_NAME_PREFIX = 'APPD_'


class AppDockerException(Exception):
    pass


class AppDocker(object):

    def __init__(self):
        self.client = Client()

    def create_run(self, app_name):
        host_control_path = os.path.join(settings.HOST_CONTROL_DIR, app_name)
        host_app_path = os.path.join(settings.HOST_APP_DIR, app_name)

        attach_volumes = [
            host_control_path + ':' + settings.CONTAINER_CONTROL_DIR,
            host_app_path + ':' + settings.CONTAINER_APP_DIR,
        ]

        container_name = CONTAINER_NAME_PREFIX + app_name

        create_args = {
            'image': CONTAINER_IMAGE,
            'tty': False,
            'detach': True,
            'mem_limit': settings.CONTAINER_MEM_LIMIT,
            'volumes': attach_volumes,
            'name': container_name,
        }

        container = self.client.create_container(**create_args)
        container_id = container.get('Id')

        if not container_id:
            raise AppDockerException("Failed to create container")

        self.client.start(container=container_id)

        return container_id
