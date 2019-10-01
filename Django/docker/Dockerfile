FROM       ubuntu:16.04
MAINTAINER h.river771@gmail.com

RUN     apt-get -y update                       #ubuntu update
RUN     apt-get -y install build-essential      #install gcc

COPY    ./client.c .
RUN     gcc client.c -o client

CMD     ./client

