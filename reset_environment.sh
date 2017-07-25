#!/bin/bash

echo "Removing the database..."
rm SigmaPi/database

echo "Remove all packages installed by pip"
sudo pip3 freeze -q | xargs sudo pip3 uninstall -yq

echo "Done resetting Django"
