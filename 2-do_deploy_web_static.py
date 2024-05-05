#!/usr/bin/python3
"""
This module contains a Fabric function that distributes an archive to my
web servers.
Archive is web_static archive created with 1-pack_web_static.py script
"""
from fabric.api import run, env, put, sudo
import os

# Specify host information
env.user = 'ubuntu'
env.hosts = ['34.229.184.178', '54.83.138.88']
env.key_filename = '~/.ssh/servers'


def do_deploy(archive_path):
    """ Distributes an archive to some web servers
    Args:
        archive_path: Path to archive to be distributed on servers
    Return:
        (bool): True if all operations have been done correctly, else False.
    """
    # If file at path archive_path does not exist, return False
    if not os.path.exists(archive_path):
        print('Path does not exist')
        return False

    # Upload the archive to /tmp/ directory of web servers
    remote_archive_path = put(archive_path, '/tmp/')[0]

    # Define relevant variables
    archive_name = remote_archive_path.split('/')[-1].split('.')[0]
    dest_folder = "/data/web_static/releases"
    path_to_decomp_archive = f'{dest_folder}/{archive_name}'
    symlink_to_curr_release = "/data/web_static/current"

    # Uncompress archive to destination folder on web server
    # run(f'sudo mkdir -p {path_to_decomp_archive}')
    # run(f'sudo chown -R ubuntu:ubuntu {path_to_decomp_archive}')
    run(f'tar -xzf {remote_archive_path} -C {dest_folder}')

    # Move decompressed files (in path_to_decomp_archive/web_static) a level up

    # Rename decompressed folder with respect to version name
    run(f'mv {dest_folder}/web_static {path_to_decomp_archive}')
    # run(f'rm -rf {path_to_decomp_archive}/web_static')

    # Remove archive from web server
    run(f'sudo rm {remote_archive_path}')

    # Delete symbolic link $symlink from server
    run(f'sudo rm {symlink_to_curr_release}')

    # Create new symbolic link to new version of code
    run(f'sudo ln -s {path_to_decomp_archive} {symlink_to_curr_release}')

    # Restart nginx
    run('sudo service nginx restart')

    # Return True if all operations exited successfully
    print('New version deployed!')
    return True
