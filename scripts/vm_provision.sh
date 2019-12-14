#!/usr/bin/env bash
# Use this to do unprivledged setup steps

echo "alias pip='python3.6 -m pip'" >> /home/vagrant/.bashrc
echo "alias dmanage='python3.6 /vagrant/sigmapiweb/manage.py'" >> /home/vagrant/.bashrc
echo "alias devl='python3.6 /vagrant/sigmapiweb/devl.py'" >> /home/vagrant/.bashrc
echo "cd /vagrant" >> /home/vagrant/.bashrc

(cd /vagrant/sigmapiweb && yes | python3.6 devl.py)