#!/bin/bash

# Install essential packages from Apt
apt-get update -y

# Python dev packages
apt-get install -y build-essential python3-dev python3-pip

# Git
apt-get install -y git

pip3 install -r /vagrant/SigmaPi/requirements.txt

# Cleanup
apt-get clean
