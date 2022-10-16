#!/bin/bash

docker build -t flask -f ./flask/Dockerfile ./
docker build -t postgresql -f ./postgresql/Dockerfile ./