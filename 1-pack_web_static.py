#!/usr/bin/python3
"""
This module contains a Fabric function that generates a .tgz archive from
the contents of the web_static folder.
"""
from fabric.api import local
from datetime import datetime


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
