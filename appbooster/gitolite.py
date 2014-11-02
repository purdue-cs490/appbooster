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
GITOLITE_CONF_REPO_TEMPLATE = """repo %s
%s
"""


def init():
    if not os.path.isdir(ADMIN_DIR):
        # TODO: clone repo to ADMIN_DIR
        pass

    if not os.path.exists(GITOLITE_CONF_FILE):
        raise RuntimeError("Cannot find gitolite.conf")

    with open(GITOLITE_CONF_FILE, 'w+') as gitolite_conf:
        gitolite_conf_content = gitolite_conf.read()

        if gitolite_conf_content != GITOLITE_CONF_DEFAULT:
            gitolite_conf.write(GITOLITE_CONF_DEFAULT)


def add_usr(user, public_key):
    # TODO: define user object model

    user_key_filename = user + '.pub'
    user_key_path = os.path.join(KEY_DIR, user_key_filename)

    with open(user_key_path, 'wb') as user_key_file:
        user_key_file.write(public_key)


def add_repo(repo, users):
    # TODO: define repo object model
    # TODO: define user object model

    repo_name = repo

    repo_conf_filename = repo_name + '.conf'
    repo_conf_path = os.path.join(CONF_DIR, repo_conf_filename)

    if isinstance(users, str):
        repo_users = [users]
    else:
        repo_users = users

    repo_users_str_buf = []
    for repo_user in repo_users:
        repo_users_str_buf.append('    RW      =   %s' % repo_user)
    repo_users_str = ''.join(repo_users_str_buf)

    repo_conf = GITOLITE_CONF_REPO_TEMPLATE % (repo_name, repo_users_str)

    with open(repo_conf_path, 'wb') as repo_conf_file:
        repo_conf_file.write(repo_conf)


if __name__ == '__main__':
    init()
