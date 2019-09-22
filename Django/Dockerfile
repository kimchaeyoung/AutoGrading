FROM       ubuntu:16.04
MAINTAINER subicura@subicura.com
RUN        apt-get -y update

RUN apt-get -y install build-essential

ENV REPO default

COPY . /
#COPY /$REPO/main.c /
#COPY /input_output/input.txt /


CMD ./runcode.sh


