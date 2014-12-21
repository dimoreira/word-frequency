#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y build-essential \
	curl \
	vim \
	git-core \
	g++ \
	make \
	libcurl4-openssl-dev \
	python \
	python-pip \
	python-software-properties \
	python-setuptools
echo -e "\e[34mInstalled essential stuff\e[0m"

pip install virtualenv
cd /vagrant
virtualenv env
