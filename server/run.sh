#!/bin/bash
sudo apt update
sudo apt install python3-pip -y
pip3 install -r requirements.txt
python3 server_s3.py
