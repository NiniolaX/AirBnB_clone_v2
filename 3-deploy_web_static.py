#!/usr/bin/python3
"""
This module contains a function that creates and distributes an archive to web
servers.
"""
from fabric.api import *
from datetime import datetime
import os

# Specify host information
env.user = 'ubuntu'
env.hosts = ['34.229.184.178', '54.83.138.88']
env.key_filename = '~/.ssh/servers'


def do_pack():
    """ Generates a .tgz archive from a specified folder
    Args:
        None
    Return:
        (str): Archive name if success, else None
    """
    # Specify source and destination folders
    src = "web_static"
    dest = "versions"

    # Get current datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Specify path to archive
    path_to_archive = f"{dest}/{src}_{timestamp}.tgz"

    # Create destination folder if it doesn't exist
    local(f'if [ ! -d {dest} ]; then mkdir {dest}; fi')

    # Run command
    result = local(f'tar -czvf {path_to_archive} {src}')
    if result.succeeded:
        return path_to_archive
    else:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to some web servers
    Args:
        archive_path: Path to archive to be distributed on servers
    Return:
        (bool): True if all operations have been done correctly, else False.
    """
    # If file at path archive_path does not exist, return False
    if not os.path.exists(archive_path):
        print(f'Path {archive_path} does not exist')
        return False

    # Upload the archive to /tmp/ directory of web servers
    remote_archive_path = put(archive_path, '/tmp/')[0]

    # Define relevant variables
    archive_name = remote_archive_path.split('/')[-1].split('.')[0]
    dest_folder = "/data/web_static/releases"
    path_to_decomp_archive = f'{dest_folder}/{archive_name}'
    symlink_to_curr_release = "/data/web_static/current"

    # Uncompress archive to destination folder on web server
    run(f'tar -xzf {remote_archive_path} -C {dest_folder}')

    # Rename decompressed folder with respect to version name
    run(f'mv {dest_folder}/web_static {path_to_decomp_archive}')
    # run(f'rm -rf {path_to_decomp_archive}/web_static')

    # Remove archive from web server
    run(f'sudo rm {remote_archive_path}')

    # Delete symbolic link $symlink from server
    run(f'sudo rm {symlink_to_curr_release}')

    # Create new symbolic link to new version of code
    run(f'sudo ln -s {path_to_decomp_archive}/ {symlink_to_curr_release}')

    # Restart nginx
    run('sudo service nginx restart')

    # Return True if all operations exited successfully
    print('New version deployed!')
    return True


def deploy():
    """Creates and distributes an archive to web servers
    Args:
        None
    Return:
        (bool): True on success, otherwise, fail
    """
    # Pack web_static
    try:
        archive_path = do_pack()
    except Exception as e:
        print(str(e))
        return False

    # Return False if no archive was created
    if archive_path is None:
        return False

    # Deploy archive
    deployment_status = do_deploy(archive_path)
    return deployment_status


if __name__ == '__main__':
    deploy()
