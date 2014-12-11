import random
import string
import subprocess

from django.contrib.auth.models import User as Auth_User
from django.db import models
from django.core.exceptions import ValidationError

import gitolite


def validate_pub(pub):
    run_script = """
        tmpf=/tmp/appbooster-$RANDOM.pub
        cat << EOF > $tmpf
%s
EOF
        ssh-keygen -l -f $tmpf
        ret=$?
        rm -f $tmpf
        exit $ret
        """ % pub
    ret = subprocess.call(['bash', '-c', run_script])
    if ret != 0:
        raise ValidationError('Not a valid public key')


class AppUserManager(models.Manager):
    def create_user(
        self,
        email,
        password,
        firstname,
        lastname,
        ssh,
    ):
        gitolite.init()
        gitolite.add_user(email, ssh)
        gitolite.commit()
        user = Auth_User.objects.create_user(
            email,
            email,
            password,
            first_name=firstname,
            last_name=lastname,
        )
        user.is_active = False
        user.save()
        appuser = self.create(
            user=user,
            public_ssh=ssh,
        )
        appuser.generate_code()
        return appuser


# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(Auth_User, primary_key=True)
    #public_ssh = models.CharField(max_length=1024, validators=[validate_pub])
    public_ssh = models.CharField(max_length=1024)
    verifycode = models.CharField(max_length=20, unique=True)

    objects = AppUserManager()

    def generate_code(self, length=10):
        v = ''.join(random.choice(string.letters + string.digits) for _ in range(length))
        while AppUser.objects.filter(verifycode=v).exists():
            v = ''.join(random.choice(string.letters + string.digits) for _ in range(length))
        self.verifycode = v
        self.save()
