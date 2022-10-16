#!/bin/bash

docker run -d -v $(pwd)/flask/app/:/app -p 5000:5000 --name flask_tests flask
docker run -d -v $(pwd)/postgresql/data/:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=admin --name postgresql_tests postgresql
