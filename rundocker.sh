#!/bin/bash

docker build -t client .
docker rm client
docker run --name="client" -it client /bin/bash
