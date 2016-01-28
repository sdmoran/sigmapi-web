# This script will deploy the latest code to production.
# This script should NOT be used if there are database migrations involved.

echo 'Creating backup of current deploy...' &&
rm -rf ~/deploy/backup && mkdir ~/deploy/backup;
cp -r ~/webapps/sigma_pi_web/SigmaPi ~/webapps/sigma_pi_web_static ~/deploy/backup;

echo 'Cloning Github repository...' &&
rm -rf ~/deploy/sigmapi-web &&
git clone https://github.com/austintrose/sigmapi-web.git ~/deploy/sigmapi-web;

echo 'Deploying site...' &&
rm -rf ~/webapps/sigma_pi_web/SigmaPi &&
cp -r ~/deploy/sigmapi-web/SigmaPi ~/webapps/sigma_pi_web &&
rm -rf ~/webapps/sigma_pi_web_static/* &&
cp -r ~/deploy/sigmapi-web/SigmaPi/static/* ~/webapps/sigma_pi_web_static &&
rm -rf ~/webapps/sigma_pi_web/SigmaPi/static &&
cp -r ~/webapps/sigma_pi_web/lib/python2.7/django/contrib/admin/static/admin ~/webapps/sigma_pi_web_static/ &&

echo 'Copying production settings file...' &&
rm -rf ~/webapps/sigma_pi_web/SigmaPi/SigmaPi/settings.py &&
cp ~/deploy/production_settings.py ~/webapps/sigma_pi_web/SigmaPi/SigmaPi/settings.py &&

echo 'Installing Python dependencies...' &&
pip2.7 install --user -r ~/webapps/sigma_pi_web/SigmaPi/requirements.txt &&
python2.7 ~/webapps/sigma_pi_web/SigmaPi/manage.py syncdb &&
python2.7 ~/webapps/sigma_pi_web/SigmaPi/manage.py migrate &&

echo 'Restarting server...' &&
~/webapps/sigma_pi_web/apache2/bin/restart &&

echo 'Deploy was successfull!';