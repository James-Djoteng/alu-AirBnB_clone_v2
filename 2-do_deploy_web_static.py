#!/usr/bin/python3
""" Function that compress a folder """
from datetime import datetime
from fabric.api import *
import shlex
import os


env.hosts = ['3.85.27.25', '107.20.35.226']
env.user = "ubuntu"


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
