# This script will deploy the latest code to production.
# This script should NOT be used if there are database migrations involved.
# Make sure this script is in "/home/sigmapiwpi/deploy" on the WebFaction server before running.

echo 'Creating backup of current deploy...' &&
rm -rf /home/sigmapiwpi/deploy/backup && mkdir /home/sigmapiwpi/deploy/backup &&
cp -r /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi /home/sigmapiwpi/webapps/sigma_pi_web_static /home/sigmapiwpi/deploy/backup &&

echo 'Cloning Github repository...' &&
rm -rf /home/sigmapiwpi/deploy/sigmapi-web &&
git clone https://github.com/austintrose/sigmapi-web.git /home/sigmapiwpi/deploy/sigmapi-web;

echo 'Deploying site...' &&
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi &&
cp -r /home/sigmapiwpi/deploy/sigmapi-web/SigmaPi /home/sigmapiwpi/webapps/sigma_pi_web &&
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web_static/* &&
cp -r /home/sigmapiwpi/deploy/sigmapi-web/SigmaPi/static/* /home/sigmapiwpi/webapps/sigma_pi_web_static &&
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/static &&
cp -r /home/sigmapiwpi/webapps/sigma_pi_web/lib/python2.7/django/contrib/admin/static/admin /home/sigmapiwpi/webapps/sigma_pi_web_static/ &&

echo 'Copying production settings file...' &&
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/SigmaPi/settings.py &&
cp /home/sigmapiwpi/deploy/production_settings.py /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/SigmaPi/settings.py &&

echo 'Installing Python dependencies...' &&
pip2.7 install --user -r /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/requirements.txt &&
python2.7 /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/manage.py syncdb &&
python2.7 /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/manage.py migrate &&

echo 'Restarting server...' &&
/home/sigmapiwpi/webapps/sigma_pi_web/apache2/bin/restart &&

echo 'Deploy was successfull!';
