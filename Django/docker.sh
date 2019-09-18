#!/bin/bash

docker build -t test . > /dev/null
docker run -ti test /runcode.sh $1 
