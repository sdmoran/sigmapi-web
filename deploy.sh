# This script will deploy the latest code to production.
# This script does NOT apply migrations. Do those yourself carefully.

echo 'Copying REPO ~/deploy/sigmapi-web-repo/SigmaPi TO PROD ~/webapps/sigma_pi_web';
cp -rf /home/sigmapiwpi/deploy/sigmapi-web-repo/SigmaPi /home/sigmapiwpi/webapps/sigma_pi_web;
echo '';

echo 'Copying REPO ~/deploy/sigmapi-web-repo/static/* TO PROD ~/webapps/sigma_pi_web_static';
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web_static/*;
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/static;
cp -rf /home/sigmapiwpi/deploy/sigmapi-web/SigmaPi/static/* /home/sigmapiwpi/webapps/sigma_pi_web_static;
echo '';

echo 'Copying admin panel static files.';
cp -r /home/sigmapiwpi/webapps/sigma_pi_web/lib/python2.7/django/contrib/admin/static/admin /home/sigmapiwpi/webapps/sigma_pi_web_static/;
echo '';

echo 'Copying production environment settings file:'
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/SigmaPi/environment_settings.py;
cp /home/sigmapiwpi/deploy/environment_settings.py /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/SigmaPi/environment_settings.py;
echo '';

echo 'Installing Python dependencies:';
pip2.7 install --user -r /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/requirements.txt;
echo '';

echo 'Restarting server...';
/home/sigmapiwpi/webapps/sigma_pi_web/apache2/bin/restart;
echo ''

echo 'Server restarted.';
