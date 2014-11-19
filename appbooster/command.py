import os
import subprocess


def run(cmd, env=None, cwd=None):
    if isinstance(cmd, str):
        cmd = cmd.split()

    envs = {}
    envs.update(os.environ)
    if env:
        envs.update(env)

    return subprocess.check_call(cmd, env=envs, cwd=cwd)


def run_script(script, env=None, cwd=None):
    return run(['/bin/bash', '-c', script], env=env, cwd=cwd)


def run_sudo_script(script, user=None, env=None, cwd=None):
    if user:
        cmd = ['/usr/bin/sudo', '-u', user]
    else:
        cmd = ['/usr/bin/sudo']

    cmd.extend(['/bin/bash', '-c', script])

    return run(cmd, env=env, cwd=cwd)
