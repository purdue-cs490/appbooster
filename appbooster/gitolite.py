import os

HOME = os.path.expanduser('~')
ADMIN_DIR = os.path.join(HOME, 'gitolite-admin')
KEY_DIR = os.path.join(ADMIN_DIR, 'keydir')
CONF_DIR = os.path.join(ADMIN_DIR, 'conf')
GITOLITE_CONF_FILE = os.path.join(CONF_DIR, 'gitolite.conf')

GITOLITE_CONF_DEFAULT = """repo gitolite-admin
    RW+     =   appbooster

include "*.conf"
"""


def init():
    if not os.path.isdir(ADMIN_DIR):
        # TODO: clone repo to ADMIN_DIR
        pass

    if not os.path.exists(GITOLITE_CONF_FILE):
        raise RuntimeError("Cannot find gitolite.conf")

    with open(GITOLITE_CONF_FILE) as gitolite_conf:
        gitolite_conf_content = gitolite_conf.read()

        if gitolite_conf_content != GITOLITE_CONF_DEFAULT:
            gitolite_conf.write(GITOLITE_CONF_DEFAULT)


def addusr(user, public_key):
    pass


if __name__ == '__main__':
    init()
