#!/bin/bash

docker-compose down --rmi all -v --remove-orphans

sudo rm -R ./postgresql/data/
sudo rm -R ./flask/app/flask_session/
mkdir ./postgresql/data

