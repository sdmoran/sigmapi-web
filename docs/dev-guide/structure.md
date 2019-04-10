# Sigma Pi, Gamma Iota Chapter Website: Project Structure

[_(Back to developer guide)_](https://github.com/sigmapi-gammaiota/sigmapi-web/tree/master/docs/dev-guide/index.md)

## The sigmapi-web directory
This is the base directory for the Sigma Pi Gamma Iota website source code. 
It contains three subdirectories and some miscellanous configuration and
information files. You can read more about the overall file structure 
[here](https://django-project-skeleton.readthedocs.io/en/latest/structure.html).

### The docs directory
You are here! The `docs` directory contains all documentation pertaining to 
this project. The `index.md` file acts as a navigation page to help you find
the documentation you need.

### The scripts directory
The `scripts` directory contains scripts to run backup and deploy operations on
the production server.

### Files
- `.gitignore`: Tells Git which files and directories shouldn't be pushed to 
the Git repository.
- `.travis.yml`: Provides instructions to Travis CI describing how to build and
test the project.
- `LICENSE`: Legally-binding contract that requires you to give us all your
money if you see our website.
- `README.md`: Basic introductory page displayed on the GitHub repository.

### The sigmapiweb directory
The `sigmapiweb` directory contains the core applications that compose our 
website. It contains five subdirectories and miscellanous configuration files.

#### The apps directory
The `apps` directory contains the bulk of the site's content and 
functionality. Each subdirectory represents a different part of the site, and
includes an individual Django application. You can read more about Django 
applications [here](https://docs.djangoproject.com/en/1.11/ref/applications/).

#### The common directory
The `common` directory contains base functionality that is used across the
website. This includes any Django settings, basic webpage templates, the root 
URLs (or routes) used to direct users to pages, and utility functions used 
across the site.

The `settings` subdirectory contains the Django settings and middleware for 
this project. The `base.py` file contains the basic settings for the Sigma Pi
Gamma Iota website; these settings are partly used in local development 
environments, but are mostly intended for use on the production server. The 
`dev.py` file can append the `base.py` file and contains settings specific to 
development environments.

The `templates/common` directory contains the basic HTML/Django templates for
all pages on the site.

The `templatetags` directory contains utility functions that are available to 
all page templates site-wide.

- `urls.py`: Contains the root URLs (page routing) for the entire site.
- `utils.py`: Contains general utility functions for use across the site.

#### The fixtures directory
The `fixtures` directory contains data to pre-populate the site's database. 
These are not used in production and are generally reserved for debugging 
purposes.

- `dev_data.json`: Contains sample data to pre-populate user, admin log 
entries, and other model info.
- `party_data.json`: Contains sample data to pre-populate a party list with 
fake names and associated information. 

#### The requirements directory
The `requirements` directory contains the Python package lists the project 
requires to run.

#### The static directory
The `static` directory contains the CSS, JS, and image resources used through 
the site. 

#### Files
- `.pylintrc`: Used to enforce code quality/cleanliness standards across the 
project via Pylint.
- `devl.py`: A cross-platform pythonic makefile substitute engineered by the 
genius Thomas Schweich.
- `manage.py`: Acts as a passthrough for devl.py. 