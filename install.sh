#!/bin/bash
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
yum update -y
yum install -y gcc gcc-c++
sudo yum install -y python35u python35u-libs python35u-devel python35u-pip
yum install -y git
yum install -y nano
pip3.5 install -r /vagrant/SigmaPi/requirements.txt

# Create a python3 alias, and set default directory
echo "alias python3=\"python3.5\"" >> .bashrc

# Set the default directory when logging in
echo "cd /vagrant/SigmaPi" >> .bash_profile
