#!/usr/bin/env python
"""
This is meant to be run on your development machine and interact with
django on a vagrant vm.

You can get tab completion in oh-my-zsh if you enable the django plugin
and add this as the last line:
    
    "compdef _managepy remote-manage.py"
"""
import os
import sys


if __name__ == "__main__":

    print "Running: \"manage.py " + " ".join(sys.argv[1:]) + "\" on Vagrant VM"

    os.system("Vagrant ssh-config > temp-vagrant-ssh-config")

    os.system("ssh -F temp-vagrant-ssh-config default python /vagrant/manage.py %s" % " ".join(sys.argv[1:]))

    os.remove("temp-vagrant-ssh-config")

