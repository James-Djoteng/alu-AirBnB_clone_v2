#!/usr/bin/python3
"""
This Fabric script distributes an archive to the web servers, based on the
1-pack_web_static.py file.
"""

from fabric.api import put, run, env
from os.path import exists

# Set the list of servers to deploy to
env.hosts = ['35.175.220.215', '54.221.18.158']


def deploy_archive(archive_path):
    """
    Distributes the archive at the specified path to the web servers.
    Returns True if the deployment was successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Extract the filename and directory name from the archive path
        filename = archive_path.split("/")[-1]
        dirname = filename.split(".")[0]

        # Set the destination directory for the archive
        dest_dir = "/data/web_static/releases/"

        # Upload the archive to the server
        put(archive_path, '/tmp/')

        # Create the destination directory for the archive
        run('mkdir -p {}{}/'.format(dest_dir, dirname))

        # Extract the archive to the destination directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(filename, dest_dir, dirname))

        # Clean up the temporary archive
        run('rm /tmp/{}'.format(filename))

        # Move the contents of the web_static directory to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(dest_dir, dirname))

        # Clean up the web_static directory
        run('rm -rf {}{}/web_static'.format(dest_dir, dirname))

        # Update the symlink to the new release
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(dest_dir, dirname))

        return True
    except:
        return False
