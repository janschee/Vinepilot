#!/bin/bash

#Install python
apt install python3.10
apt install python3.10-venv

#Build virtual environment
mkdir ./venv
python3.10 -m venv ./venv

#Install requirements
venv/bin/python -m pip install -r ./requirements.txt


