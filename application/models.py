from django.db import models
from appbooster.models import AppUser

from appbooster import gitolite

PORT_START = 18000
PORT_END = 18099

class ApplicationManager(models.Manager):
    def create_app(
        self,
        name,
        user,
    ):
        git_repo = gitolite.add_repo(name, [user.email,])
        gitolite.commit()
        app = self.create(
            name=name,
            apptype='python',
            port_num=get_port_num(),
            wsgi_module='wsgi',
            git_repo=git_repo,
        )
        app.appusers.add(user.appuser)
        return app

    def get_port_num(self):
        for port in xrange(PORT_START,PORT_END+1):
            if not Application.objects.filter(port_num=port).exists():
                return port
        return 0


# Create your models here.
class Application(models.Model):
    # TODO
    name = models.CharField(max_length=50)
    appusers = models.ManyToManyField(AppUser)
    container_id = models.CharField(max_length=100)
    apptype = models.CharField(max_length=30)
    port_num = models.IntegerField(unique=True)
    wsgi_module = models.CharField(max_length=256)
    git_repo = models.CharField(max_length=256)

    objects = ApplicationManager()