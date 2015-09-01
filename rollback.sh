# This script will restore the site from whatever is in the /home/sigmapiwpi/deploy/backup folder.
# This should ONLY be used immediately after running deploy.sh if production is in error.
# Make sure this script is in "/home/sigmapiwpi/deploy" on the WebFaction server before running.

rm -rf /home/sigmapiwpi/webapps/sigma_pi_web/SimgaPi &&
cp -r /home/sigmapiwpi/deploy/backup/SigmaPi /home/sigmapiwpi/webapps/sigma_pi_web &&
rm -rf /home/sigmapiwpi/webapps/sigma_pi_web_static/* &&
cp -r /home/sigmapiwpi/deploy/backup/sigma_pi_web_static/* /home/sigmapiwpi/webapps/sigma_pi_web_static &&
pip2.7 install --user -r /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/requirements.txt &&
python2.7 /home/sigmapiwpi/webapps/sigma_pi_web/SigmaPi/manage.py syncdb &&
/home/sigmapiwpi/webapps/sigma_pi_web/apache2/bin/restart;
