
PYTHON=python3.6
PIP=sudo pip3.6
MANAGE=$(PYTHON) manage.py
DEV_DATA=fixtures/dev_data.json

dev: requirements loaddata static

requirements:
	$(PIP) install -q -r requirements.txt

loaddata: syncdb
	$(MANAGE) loaddata $(DEV_DATA)

dumpdata: syncdb
	$(MANAGE) dumpdata --natural-foreign -e contenttypes -e auth.Permission > $(DEV_DATA)

syncdb:
	$(MANAGE) migrate --run-syncdb

run: migrate static quickrun

static:
	$(MANAGE) collectstatic

migrate:
	$(MANAGE) migrate

quickrun:
	$(MANAGE) runserver 0.0.0.0:8000

test:
	echo lol what tests

newmigrations:
	$(MANAGE) makemigrations
	@echo ====================================================================
	@echo Now before you commit, rename those migrations \(if any were made\).
	@echo Don\'t leave it as \'0003_auto_20170101_1942.py\', you animal.
	@echo Be civilized. Change it to something like \'0003_add_blacklist.py\'.
	@echo ====================================================================

superuser:
	$(MANAGE) createsuperuser

dbshell:
	$(MANAGE) dbshell

shell:
	$(MANAGE) shell

destroyenv: clean
	rm database
	$(PIP) freeze -q | xargs $(PIP) uninstall -yq

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -exec rm {} +
