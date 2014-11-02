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

COMMENT_ADD_USER_TEMPLATE = "Added user %s."
COMMENT_ADD_REPO_TEMPLATE = "Added repo %s for %s."
COMMENT_REMOVE_USER_TEMPLATE = "Removed user %s."
COMMENT_REMOVE_REPO_TEMPLATE = "Removed repo %s."


class GitoliteException(Exception):
    pass


def _commit(comment):
    """Git commit.
    """
    # TODO: waiting on git module
    pass


def commit():
    """Commit changes. Call this method after any of the operations.

    Git push.
    """
    # TODO: waiting on git module

    git_dir = os.path.join(ADMIN_DIR, '.git')

    pass


def init():
    if not os.path.isdir(ADMIN_DIR):
        # TODO: clone repo to ADMIN_DIR
        pass

    if not os.path.exists(GITOLITE_CONF_FILE):
        raise GitoliteException("Cannot find gitolite.conf")

    with open(GITOLITE_CONF_FILE, 'w+') as gitolite_conf:
        gitolite_conf_content = gitolite_conf.read()

        if gitolite_conf_content != GITOLITE_CONF_DEFAULT:
            gitolite_conf.write(GITOLITE_CONF_DEFAULT)


def add_user(user, public_key):
    # TODO: define user object model

    user_name = user

    user_key_filename = user_name + '.pub'
    user_key_path = os.path.join(KEY_DIR, user_key_filename)

    if os.path.exists(user_key_path):
        raise GitoliteException("%s user key file already exists" % user_key_filename)

    with open(user_key_path, 'wb') as user_key_file:
        user_key_file.write(public_key)

    comment = COMMENT_ADD_USER_TEMPLATE % user_name
    _commit(comment)


def add_repo(repo, users):
    # TODO: define repo object model
    # TODO: define user object model

    repo_name = repo

    repo_conf_filename = repo_name + '.conf'
    repo_conf_path = os.path.join(CONF_DIR, repo_conf_filename)

    if isinstance(users, str):
        repo_user_names = [users]
    else:
        repo_user_names = users

    repo_user_names_str_buf = []
    for repo_user_name in repo_user_names:
        repo_user_names_str_buf.append('    RW      =   %s' % repo_user_name)
    repo_user_names_str = ''.join(repo_user_names_str_buf)

    repo_conf = GITOLITE_CONF_REPO_TEMPLATE % (repo_name, repo_user_names_str)

    with open(repo_conf_path, 'wb') as repo_conf_file:
        repo_conf_file.write(repo_conf)

    comment = COMMENT_ADD_REPO_TEMPLATE % (repo_name, ', '.join(repo_user_names))
    _commit(comment)


def rm_user(user):
    # TODO: define user object model

    user_name = user

    user_key_filename = user_name + '.pub'
    user_key_path = os.path.join(KEY_DIR, user_key_filename)

    if not os.path.exists(user_key_path):
        raise GitoliteException("%s user key file cannot be found" % user_key_filename)

    os.remove(user_key_path)

    comment = COMMENT_REMOVE_USER_TEMPLATE % user_name
    _commit(comment)


def rm_repo(repo):
    # TODO: define repo object model

    repo_name = repo

    repo_conf_filename = repo_name + '.conf'
    repo_conf_path = os.path.join(CONF_DIR, repo_conf_filename)

    if not os.path.exists(repo_conf_path):
        raise GitoliteException("%s repo conf file cannot be found" % repo_name)

    os.remove(repo_conf_path)

    comment = COMMENT_REMOVE_REPO_TEMPLATE % repo_name
    _commit(comment)


if __name__ == '__main__':
    init()
