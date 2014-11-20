import os

from django.conf import settings
from django.db import models

from appbooster import gitolite
from appbooster.models import AppUser


class ApplicationManager(models.Manager):

    def create_app(
        self,
        name,
        user,
    ):
        git_repo = gitolite.add_repo(name, [user.email])
        gitolite.init()
        gitolite.commit()
        app = self.create(
            name=name,
            apptype='python',
            port_num=self.get_port_num(),
            wsgi_module='wsgi',
            git_repo=git_repo,
        )
        app.appusers.add(user.appuser)
        return app

    def get_port_num(self):
        for port in xrange(settings.APP_PORT_START, settings.APP_PORT_END+1):
            if not Application.objects.filter(port_num=port).exists():
                return port
        return 0


# Create your models here.
class Application(models.Model):
    # TODO
    name = models.CharField(max_length=50, unique=True)
    appusers = models.ManyToManyField(AppUser)
    container_id = models.CharField(max_length=100)
    apptype = models.CharField(max_length=30)
    port_num = models.IntegerField(unique=True)
    wsgi_module = models.CharField(max_length=256)
    git_repo = models.CharField(max_length=256)

    objects = ApplicationManager()

    @property
    def local_repo_path(self):
        return os.path.join(settings.HOST_APP_DIR, self.name, self.name)

    @property
    def host_control_path(self):
        return os.path.join(settings.HOST_CONTROL_DIR, self.name)

    @property
    def host_app_path(self):
        return os.path.join(settings.HOST_APP_DIR, self.name)

    @property
    def host_nginx_config_path(self):
        return os.path.join(settings.NGINX_CONFIG_DIR, self.name)
