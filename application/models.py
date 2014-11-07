from django.db import models
from appbooster.models import AppUser

# Create your models here.
class Application(models.Model):
    # TODO
    name = models.CharField(max_length=50)
    appuser = models.OneToOneField(AppUser)
    container_id = models.CharField(max_length=100)
    apptype = models.CharField(max_length=30)
    port_num = models.IntegerField(unique=True)
    wsgi_module = models.CharField(max_length=256)
    git_repo = models.CharField(max_length=256)