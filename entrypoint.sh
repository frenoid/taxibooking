#!/bin/bash
docker rm $(docker stop $(docker ps -a -q --filter ancestor=motional --format="{{.ID}}"))
docker build -t motional .
docker run -d -p 8080:8080 motional