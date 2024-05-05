#!/usr/bin/python3
"""
This module contains a Fabric function that distributes an archive to my
web servers.
Archive is web_static archive created with 1-pack_web_static.py script
"""
from fabric.api import run, env, put
import os


def do_deploy(archive_path):
    """ Distributes an archive to some web servers
    Args:
        archive_path: Path to archive to be distributed on servers
    Return:
        (bool): True if all operations have been done correctly, else False.
    """
    if not os.path.exists(archive_path):
        # If file at path archive_path does not exist, return False
        return False

    # Define host information
    env.user = 'ubuntu'
    env.hosts = ['34.229.184.178', '54.83.138.88']

    # Define relevant variables
    archive_name = archive_path.split('/')[-1].split('.')[0]
    destination_folder = "/data/web_static/releases"
    path_to_decomp_archive = f'{destination_folder}/{archive_name}/'
    symlink_to_curr_release = "/data/web_static/current"

    # Upload the archive to /tmp directory of web servers
    put(f'{archive_path}, /tmp/')

    # Uncompress archive to destination folder on web server
    run(f'sudo mkdir -p {path_to_decomp_archive}')
    run(f'tar -xzf /tmp/{archive_name} -C {path_to_decomp_archive}')

    # Remove archive from web server
    run(f'sudo rm /tmp/{archive_name}.tgz')

    # Delete symbolic link $symlink from server
    run(f'sudo rm {symlink_to_curr_release}')

    # Create new symbolic link to new version of code
    run(f'ln -s {path_to_decomp_archive} {symlink_to_curr_release}')

    # Restart nginx
    run('sudo service nginx restart')

    # Return True if all operations exit successfully
    return True
