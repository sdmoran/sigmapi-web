# Sigma Pi Gamma Iota Chapter's website

This Python Django application powers the Sigma Pi Gamma Iota Chapter's website, which can be found at: https://sigmapigammaiota.org/

This project uses [Vagrant](https://www.vagrantup.com/) to keep the build environment standard between developers. In particular, I would recommend you install [Vagrant 1.6.3](https://www.vagrantup.com/download-archive/v1.6.3.html).

## First time setup

These steps will walk you through deploying the site on your local machine for the first time.

1.
  Clone the repository.

  ```
  $ git clone git@github.com:austintrose/sigmapi-web.git

  ...

  $ cd sigmapi-web
  ```

2.
  Create the Vagrant VM. Note that this may take a few minutes, and a lot of text will fly by.

  ```
  $ vagrant up
  ```

3.
  Open up a shell on the virtual machine, and navigate to the shared folder.

  ```
  $ vagrant ssh

  ...

  $ cd /vagrant/SigmaPi
  ```

4.
  Create the database. Note that you will need to follow the prompts to create an admin user account. This is only for your local machine, so you don't need to worry about what you put here but you should remember it.

  ```
  $ python manage.py syncdb
  ```

5.
  Collect static assets (CSS, JS, images, etc.).

  ```
  $ python manage.py collectstatic
  ```

6.
  Run Django.

  ```
  $ python manage.py runserver 0.0.0.0:8000
  ```

7.
  Open a web browser on your computer, and navigate to localhost:8000 to view the site. You can make changes to the code and your running instance will be updated automatically. You can log into the site with the admin account credentials you created earlier.

  When you are done working, it is best to run `vagrant suspend` from your host (not from the VM) in order to stop the VM from running in the background. Later you can `vagrant resume` to bring the VM back to the state it was in previously.


## Deploying to WebFaction

1.
  SSH into our WebFaction box. Credentials are redacted, contact @austintrose if you need them.

  ```
  $ ssh our_username@our.webfactional.url
  ```

2.
  Navigate to the deploy folder, and run the deploy script.

  ```
  $ cd deploy
  $ ./deploy.sh
  ```

  Note that the `deploy.sh` script in that folder should be a copy of the one in this repository. It is kept here for version controlling.

  At this point you should be *done*, unless...

3.
  There may be warnings on deploy, but if there is a failure in production after deployment then you should perform a rollback. In the same directory as the `delpoy.sh` script is `rollback.sh`, which will revert production to its previous deploy.

Note that there are additional complications if you wish to deploy a code change which requires a database migration. For now defer to @austintrose for that.
