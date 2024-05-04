#!/usr/bin/python3
"""
Script generates a .tgz archive from the contents of the web_static folder

Functions:
    do_pack: Generates .tgz archives of a specified folder
"""
from fabric.api import local
from datetime import datetime


@task
def do_pack():
    """ Generates a .tgz archive from a specified folder
    Args:
        None
    Return:
        str: Archive name
    """
    # Get current datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    source = "web_static"
    destination = "versions"

    # Create destination folder if it doesn't exist
    local(f"if [ ! -d {destination} ]; then mkdir {destination}; fi")
    archive_name = f"{destination}/{source}_{timestamp}.tgz"

    # Run command
    result = local(f"tar -cvzf {archive_name} {source_file}")
    if result.succeeded:
        return archive_name
    else:
        return None
