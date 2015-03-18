#!/bin/bash

# Install essential packages from Apt
apt-get update -y

# Python dev packages
apt-get install -y build-essential python python-dev python-setuptools python-pip

# Git
apt-get install -y git

# virtualenv global setup
if ! command -v pip; then
    easy_install -U pip
fi
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    easy_install virtualenv virtualenvwrapper stevedore virtualenv-clone
fi

# Install our Python packages in a temporary virtual env so that they'll get cached.
if [[ ! -e /home/vagrant/.pip_download_cache ]]; then
    su - vagrant -c "mkdir -p /home/vagrant/.pip_download_cache && \
        virtualenv /home/vagrant/yayforcaching && \
        PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache /home/vagrant/yayforcaching/bin/pip install -r /vagrant/SigmaPi/requirements.txt && \
        rm -rf /home/vagrant/yayforcaching"
fi

# Cleanup
apt-get clean
