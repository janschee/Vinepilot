#!/bin/bash

#Install python
apt install python3.10
apt install python3.10-venv

#Install dependencies
sudo apt-get install libcairo2 libcairo2-dev #Cairo
sudo apt install libgl1-mesa-glx #OpenCV

#Build virtual environment
mkdir ./venv
python3.10 -m venv ./venv

#Install requirements
venv/bin/python -m pip install -r ./requirements.txt


