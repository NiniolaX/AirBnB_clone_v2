#!/usr/bin/python3
"""
This Fabric script distributes compressed static code files (archive) to
some web servers.
"""
from fabric.api import put, run, env
import os

env.user = 'ubuntu'
env.hosts = ['34.229.184.178', '54.83.138.88']
env.key_filename = '~/.ssh/servers'


def do_deploy(archive_path):
    """Distributes an archive to web servers.
    Args:
        archive_path(str): Local path to archive
    Return:
        (bool): True on success, otherwise, False
    """
    try:
        # Check if passed archive path exists
        if not os.path.exists(archive_path):
            print(f'File {archive_path} not found')
            return False

        # Extract necessary paths
        archive_name = os.path.basename(archive_path)
        tmp_folder = '/tmp/'
        dest_folder = '/data/web_static/releases/'
        release_symlink = '/data/web_static/current'
        uncomp_folder_path = f'{dest_folder}/{archive_name}'.split('.')[0]

        # Upload archive file to temporary folder (/tmp/)
        put(archive_path, tmp_folder)

        # Create destination folder if it doesn't exist
        run(f'if [ ! -d {dest_folder} ]; then sudo mkdir {dest_folder}; fi')

        # Uncompress archive in temporary folder to destination folder
        run(f'tar -xzf {tmp_folder}/{archive_name} -C {dest_folder}')
        # Rename uncompressed folder
        run(f'mv {dest_folder}/web_static {uncomp_folder_path}')

        # Delete archive from web server
        run(f'rm -rf {tmp_folder}/{archive_name}')

        # Update symbolic link to current release
        run(f'sudo rm -rf {release_symlink}')
        run(f'sudo ln -s {uncomp_folder_path}/ {release_symlink}')

        # Update Nginx configuration to serve new release to hbnb_static
        config_file = "/etc/nginx/sites-available/default"
        hbnb_block = f'''
            location /hbnb_static {{
                alias {release_symlink}/;
                index index.html;
            }}
        '''
        cmd = 'sudo sed -i "/^   location \\/ {{$/i\\{hbnb_block}" {config_file}'
        run(cmd)

        # Restart server
        run('sudo service nginx restart')

        print('New version deployed!')
        return True

    except Exception as e:
        print(f'Error during deployment: {e}')
        return False
