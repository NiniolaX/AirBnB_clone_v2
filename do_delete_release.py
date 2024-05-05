#!/usr/bin/python3
from fabric.api import run, env

env.user = 'ubuntu'
env.hosts = ['34.229.184.178', '54.83.138.88']
env.key_filename = '~/.ssh/servers'

def delete_release():
    path_to_release = "/data/web_static/releases/web_static_20240504152331"

    # Delete release folder
    run(f'rm -rf {path_to_release}')

    # Delete symbolink link to release
    run(f'sudo rm -rf /data/web_static/current')

    # Revert link to test folder
    run(f'sudo ln -s /data/web_static/releases/test/ /data/web_static/current')

    print('Release succesfully deleted.')
