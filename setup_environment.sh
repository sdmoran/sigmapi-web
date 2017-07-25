#!/bin/bash
cd /vagrant/SigmaPi

echo "Installing python packages"
pip3 install -q -r requirements.txt

echo "Running syncdb..."
python3 manage.py syncdb

echo "Loading Fixtures..."
python3 manage.py loaddata fixtures/dev_data.json

echo "Collecting static resources"
python3 manage.py collectstatic

