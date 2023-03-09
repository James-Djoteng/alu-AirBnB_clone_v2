#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the function do_deploy.
"""

import os
from fabric.api import env, put, run
from datetime import datetime


env.hosts = ['3.85.27.25', '107.20.35.226']
env.user = 'ubuntu'

def do_pack():
    """Return the archive path when correctly generated"""
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        t = datetime.now()
        f = "%Y%m%d%H%M%S"
        archive_path = 'versions/web_static_{}.tgz'.format(t.strftime(f))
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        remote_path = '/data/web_static/releases/{}'.format(archive_name)
        run('sudo mkdir -p {}'.format(remote_path))
        run('sudo tar -xzf /tmp/{} -C {} --strip-components=1'.format(archive_filename, remote_path))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('sudo rm -f /data/web_static/current')

        # Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
        run('sudo ln -s {} /data/web_static/current'.format(remote_path))

        return True
    except:
        return False
