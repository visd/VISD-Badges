#!/usr/bin/env bash

PROJECT_NAME=VISD_Badges

# Shared Folder
rm -rf /var/www
ln -fs /vagrant /var/www

# Updates
apt-get -yq update
apt-get -yq upgrade

# Server componets 
apt-get -yq install apache2

# Database componets
# apt-get -yq install postgresql libpq-dev build-dep python-psycopg2

# Python
apt-get -yq install python-pip python-dev

# Set up virtualenv
pip install -q virtualenv

virtualenv /home/vagrant/.virtualenvs/$PROJECT_NAME

source /home/vagrant/.virtualenvs/$PROJECT_NAME/bin/activate

# Rereirements for app
/home/vagrant/.virtualenvs/VISD_Badges/bin/pip install -r /vagrant/Manifest/requirements.pip

# Make virtualenvs owned by vagrant user
chown -R vagrant:vagrant /home/vagrant/.virtualenvs
