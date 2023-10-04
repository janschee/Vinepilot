#!/bin/bash

#Install python
apt install python3.10

#Build virtual environment
mkdir ./venv
python3.10 -m venv ./venv

#Install requirements
venv/bin/python -m pip install -r ./requirements.txt


