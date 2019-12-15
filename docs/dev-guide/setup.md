# Sigma Pi, Gamma Iota Chapter Website: Installation & Setup

[_(Back to developer guide)_](https://github.com/sigmapi-gammaiota/sigmapi-web/tree/master/docs/dev-guide/index.md)

## Dependencies

* [Git](https://git-scm.com/downloads): Version control system.
  The latest version is recommended.
* [Python 3.6.*](https://www.python.org/downloads/): The primary language
  used in the development of the website.
  * [Library: venv](https://docs.python.org/3.6/library/venv.html) [optional]: Used to
    create a virtual environment to isolate the development python from the
    system-wide python.
* Python libraries as described in [`requirements/base.txt`](https://github.com/sigmapi-gammaiota/sigmapi-web/blob/master/sigmapiweb/requirements/base.txt) and, for developers, [`requirements/dev.txt`](https://github.com/sigmapi-gammaiota/sigmapi-web/blob/master/sigmapiweb/requirements/base.txt). These are installed automatically by the `devl.py` script.
  * Several of these libraries require a C/C++ compiler. If you are using Windows, you may need to install one. The easiest way is to either use WSL (described below) or install Visual Studio Dev Tools from https://visualstudio.microsoft.com/downloads/.

This guide will use `python3.6` to denote the Python interpreter on the command line. Note that it may be aliased as `python`, `python3`, `py`, or some other name on your system. If this is the case, replace `python3.6` in commands below with the alias of your interpreter.

### Additional Dependencies for Windows Developers

If you are using a Windows computer, it is recommended that you use the Windows Subsystem for Linux. For instructions on setting up this environment, see [Appendix: WSL Setup](#appendix-wsl-setup). After completing the instructions, follow the steps outlined in [First Time Setup](#first-time-setup).

## First Time Setup

These steps will walk you through deploying the site on your local machine for the first time.

### 1. Clone the repository.
If you use ssh keys to authenticate with github, use the following (If you don't know what this means, use the alternate method below):
```bash
$ git clone git@github.com:sigmapi-gammaiota/sigmapi-web.git
...
$ cd sigmapi-web
```
Alternate method using HTTPS:
```bash
$ git clone https://github.com/sigmapi-gammaiota/sigmapi-web.git
...
$ cd sigmapi-web
```


### 2. [Optional] Create a seprate coding environment.

#### A) Create and activate the Python virtual environment.

This creates a local python virtualenv and activates it. This is recommended in order to isolate this Python environment from any others which are on your computer currently or may be installed in the future.

Windows:

```cmd
> python3.6 -m venv .\venv
> venv\bin\activate
```

Linux/Mac/WSL/Other Systems Using Bash:

```bash
$ python3.6 -m venv ./venv
$ source venv/bin/activate
```

#### B) Use a Vagrant box.

[Vagrant](https://www.vagrantup.com/) is a tool for creating identical production and development envrionments. It will create a VM (managed by virtualbox) that you can interact with the `vagrant` command on your command line

For all systems:

1. Install [Virtualbox](https://www.virtualbox.org/)
   1. You may need to enable hardware virtualization in your BIOS
2. Install Vagrant (linked above)

For a first time run:
```bash
$ vagrant plugin install vagrant-vbguest
$ vagrant up
```

The `devl.py` script will be run for you, so you can skip step 3.

To continue following along in the setup, execute

```bash
$ vagrant ssh
```

to be dropped into your VM.

Extra Vagrant info:
  - To 'freeze' your vm when you are done developing
    - `vagrant suspend`
  - To start your vm from off or a suspended state
    - `vagrant up`
  - To completely turn off your vm
    - `vagrant halt`
  - To fix some sync issues or restart the vm:
    - `vagrant reload`
  - To nuke your vm from orbit:
    -  `vagrant destroy`
  - The correct ports have been forwarded so you'll be able to access the website as described below.

### 3. Set up the development environment

Run the `devl.py` script. The script will detect that it has not yet been set up and will attempt to automatically determine what variables are needed for your system. After it has done so, it will place them in a file called `devl_settings.json` which you can modify to your liking. It will also guide you through the completion of your development environment setup if necessary. After doing this, answering `y` or simply pressing `ENTER` when asked if you would like to run `dev` will install the Python package requirements, load initial data for the database, and collect static files.

```bash
$ cd sigmapiweb
$ python3.6 devl.py
...
Would you like to run `dev` now to install your environment?
> y
```

Note that the tools `devl.py` uses can be changed at any time in the future by modifying the variables placed in `devl_settings.json` after this step.

### 4. Run Django.

This step is handled by `devl.py`. You can use this command any time in the future while developing to view changes to the site locally.

```bash
$ python3.6 devl.py run
```

### 5. Open a web browser on your computer, and navigate to localhost:8000 to view the site.

You can make changes to the code and your running instance will be updated automatically. You can log into the site with the admin account credentials you created earlier.  **NOTE:** Though changes will automatically update, JS and CSS resources will get cached and require a redownload using `ctrl-F5`.

When you're done, you can kill the server with `ctrl-c`. 

If you are using python virtualenv, deactivate it with:

```bash
$ deactivate
```

## Using the Database

You should familiarize yourself with the database via the local [Admin Panel](localhost:8000/admin) on your local site. It is available anytime you run the server (use `python3.6 devl.py run`).

## Fixture Data

Sample database entries are provided to aid in development and testing. They are automatically loaded by `python3.6 devl.py dev`, or you can load/reload them manually using:

```bash
$ python3.6 devl.py loaddata
```

When you load the dev fixture data, the following users are created (along with their associated groups):

```
admin:password # The admin user.
brother:brother # A regular active brother account.
first:first # The first counselor.
second:second # The second counselor.
third:third # The third counselor.
fourth:fourth # The fourth counselor.
alumnichair:alumnichair # The alumni relations chair.
newmember:newmember # A new member.
bacchair:bacchair # The BAC chair.
housemanager:housemanager # The house manager.
parliamentarian:parliamentarian # The parliamentarian.
philanthropychair:philanthropychair # The philanthropy chair.
rushchair:rushchair # The rush chair.
sage:sage # The sage.
scholarshipchair:scholarshipchair # The scholarship chair.
socialchair:socialchair # The social chair.
steward:steward # The steward.
```

These accounts will be modifiable from the Admin Panel in your local site.

### Updating Fixture Data

```bash
$ python3.6 devl.py dumpdata
```

This approximates the following bash command:

```bash
python3 manage.py dumpdata --natural-foreign -e contenttypes -e auth.Permission > fixtures/dev_data.json
```

> --natural-foreign will use a more durable representation of foreign keys (ex. User.username instead of User.id)

> -e flags are used to exclude contenttypes and permissions, which are already generated by syncdb

### Appendix: WSL Setup

Developers using Windows 10 should consider using the Windows Subsystem for Linux for site development. You can find
the installation and setup documentation [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10).
Choosing Ubuntu as your subsystem is recommended if you're new to Linux.

After installing the subsystem, you can access the Linux bash by opening a
command prompt or PowerShell and entering:
```bash
> bash
```

Run the following to update your packages and install all development dependencies:
```bash
$ sudo apt update && sudo apt upgrade
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
$ sudo apt-get install python3.6 python3-pip python3.6-dev python3.6-venv
```

In some cases, the subsystem will refuse to recognize Python 3.6 as the correct version
when you run `$ python3 -V`. This can be solved with Ubuntu's update-alternatives, which allows
you to select which version of Python 3 the `$ python3` command references.

```bash
$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python3 get-pip.py --force-reinstall
```

You can then toggle between each version of python with the following command. Beware: you may
have to re-install pip with the final two commands above each time you switch.

```bash
$ sudo update-alternatives --config python3
```

Once you have completed the installations, use the WSL terminal to continue from [First Time Setup](#first-time-setup).
