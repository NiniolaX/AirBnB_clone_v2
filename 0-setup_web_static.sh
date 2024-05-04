#!/usr/bin/env bash
# Prepares web servers for deployment of static content (i.e. web_static)

# Install Nginx if it is not already installed
if ! sudo service nginx status; then
	sudo apt -y update
	sudo apt -y install nginx
	sudo service nginx start
fi

# Create /data/ directory and necessary subdirectories if they don't exist
webstatic_dir="/data/web_static"
if [ ! -d "$webstatic_dir/releases" ]; then
	sudo mkdir -p "$webstatic_dir/releases"
fi

if [ ! -d "$webstatic_dir/shared" ]; then
	sudo mkdir -p "$webstatic_dir/shared"
fi

if [ ! -d "$webstatic_dir/releases/test" ]; then
	sudo mkdir -p "$webstatic_dir/releases/test"
fi

# Create a fake HTML file to be served
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > "$webstatic_dir/releases/test/index.html"

# Create a symbolic link to /data/web_static/releases/test/ directory
if [ -L "$webstatic_dir/current" ]; then
	sudo rm "$webstatic_dir/current"
fi
sudo ln -s "$webstatic_dir/releases/test/" "$webstatic_dir/current"

# Give ownership of /data/ folder to 'ubuntu' user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current to hbnb_static
hbnb_location_block="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t}\n"
sudo sed -i "/error_page/a\ $hbnb_location_block" /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart
