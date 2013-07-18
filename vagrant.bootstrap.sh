#!/usr/bin/env bash

PROJECT_NAME=VISD_Badges


# Updates
apt-get -yq update
apt-get -yq upgrade

# Server componets 
apt-get -yq install apache2

# Python
apt-get -yq install python-pip python-dev

# Rereirements for app
pip install -r /vagrant/Manifest/requirements.pip

# Shared Folder
rm -rf /var/www
ln -fs /vagrant /var/www