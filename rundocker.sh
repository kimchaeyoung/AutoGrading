#!/bin/bash

docker build -t client .
docker rm docker
docker run --name="docker" -it client /bin/bash
