REQUIREMENTS_FILE	:= requirements.txt
GALAXY_FILE		:= collections.yml
GIT_ROOT		:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VENV_ROOT		:= $(PWD)/.venv
export VENV		?= $(VENV_ROOT)
all: setup

venv $(VENV):  # creates $(VENV) folder if does not exist
	python3 -mvenv $(VENV)
	$(VENV)/bin/pip install -U pip setuptools

$(MAIN_CLI_PATH) $(VENV)/bin/nosetests $(VENV)/bin/python $(VENV)/bin/pip: # installs latest pip
	test -e $(VENV)/bin/pip || $(MAKE) $(VENV)
	$(MAKE) setup

setup: | venv $(VENV)/bin/pip
	$(VENV)/bin/pip install --force-reinstall -r $(REQUIREMENTS_FILE)
	$(VENV)/bin/ansible-galaxy collection install -r $(GALAXY_FILE) --force

config-build:
	$(VENV)/bin/ansible-playbook playbooks/atd-fabric-deploy.yml --tags "build"

config-deploy:
	$(VENV)/bin/ansible-playbook playbooks/atd-fabric-deploy.yml --tags "deploy_eapi"