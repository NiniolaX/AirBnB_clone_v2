#!/usr/bin/env bash
# Prepares web servers for deployment of static content (i.e. web_static)

# Install Nginx if it is not already installed
echo "Checking if nginx exists and is running..."
if ! sudo service nginx status; then
	echo "Installing, nginx..."
	sudo apt -y update
	sudo apt -y install nginx
	sudo service nginx start
fi

# Create function that creates a specified directory if it doesn't exist
create_dir() {
	local dir="$1"
	if [ ! -d "$dir" ]; then
		echo "Creating $dir directory..."
		sudo mkdir "$dir"
	else
		echo "Directory $dir already exists."
	fi
}

# Create variables for files/dir that will be reused
test_dir="/data/web_static/releases/test"
current_sym_link="/data/web_static/current"

# Create /data/ directory and necessary subdirectories if they don't exist
create_dir "/data/"
create_dir "/data/web_static"
create_dir "/data/web_static/releases"
create_dir "/data/web_static/shared"
create_dir "$test_dir"

# Create a fake HTML file to be served
if [ ! -f "$test_dir/index.html" ]; then
	echo "Creating fake html file..."
	echo "Holberton School" > "$test_dir/index.html"
else
	echo "Fake html file ($test_dir/index.html) already exists."
fi

# Create a symbolic link to /data/web_static/releases/test/ directory
if [ -L "$current_sym_link" ]; then
	echo "Deleting symbolink link..."
	sudo rm "$current_sym_link"
fi
echo "Creating symbolic link..."
sudo ln -s "$test_dir/" "$current_sym_link"


# Give ownership of /data/ folder to 'ubuntu' user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of $current_sym_link to hbnb_static
hbnb_location_block="\n\tlocation /hbnb_static {\n\t\talias $current_sym_link/;\n\t\tindex index.html;\n\t}\n"
sudo sed -i "/^\tlocation \/ {$/i\ $hbnb_location_block" /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart
