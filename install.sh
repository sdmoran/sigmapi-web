#!/bin/bash

# Add custom Python repo in order to get latest Python packages
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
yum update -y

# Install Python development packages
yum install -y gcc gcc-c++
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
pip3.6 install -r /vagrant/SigmaPi/requirements.txt

# Install other utilities
yum install -y git
yum install -y nano  # Learn vi noobs...

# Fix problem where site doesn't load after install
iptables -F

# Create a python3 alias, and set default directory
echo "alias python3=\"python3.6\"" >> /home/vagrant/.bashrc

# Set the default directory when logging in
echo "cd /vagrant/SigmaPi" >> /home/vagrant/.bash_profile
