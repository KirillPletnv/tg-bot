#!/bin/bash

rm -rf CICDFirst
git clone git@gitlab.com:cicd5462412/CICDFirst.git
cd  CICDFirst
python3 -m main.py
