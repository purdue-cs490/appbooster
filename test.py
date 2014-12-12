import subprocess

# test.py
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
    print ret


validate_pub("")
validate_pub("aaa")
validate_pub("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAl/inM48IEFZKsbEqeyx60sj20w2EZrioJVEim1PoodakjM4bDbDSO1Vxtv8XFGyF+T4ifJ80vAgQ8aOGYI6fXRZX4yHdazdCkBRm1UY6fwe5UVJxfIx6q2ubd+xASfL+S5vq5WnlfifaG6/RgJ/Rz/cS4sVj8AdtZa7M1lvoLoxWGdSd9DxfwnH9Ykcy3EP2guMjKuUjqQjh3QGDCi9I9ysrcNG8b9CL1jQ5vlxj2wiqnG3ZvoAliCDcipXh/TQPZuXW4TQt/9DpU9MjuAaxT3TKs0n3a2hG5gsDI+oChD5KAY0cFL4W96Z5n1oRL3Stt8uJD4XirWXieCJ5qbPv chen769@borg15.cs.purdue.edu")