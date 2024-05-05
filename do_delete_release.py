#!/usr/bin/python3
"""
This module contains a Fabric function that deletes a release from a server.
"""

from fabric.api import run, env

env.user = 'ubuntu'
env.hosts = ['34.229.184.178', '54.83.138.88']
env.key_filename = '~/.ssh/servers'


def delete_release(path_to_release):
    """ Deletes a release from a server.
    Args:
        path_to_release: Full path to folder containing release codebase
    Return:
        None
    """
    # Delete release folder
    run(f'rm -rf {path_to_release}')

    # Delete symbolic link link to release
    run(f'sudo rm -rf /data/web_static/current')

    # Restore symbolic link to test folder
    run(f'sudo ln -s /data/web_static/releases/test/ /data/web_static/current')

    print('Release succesfully deleted.')
