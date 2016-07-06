# Base image
FROM ubuntu:latest

# get dependencies
RUN apt-get update \
  && apt-get install -y wget \
  && apt-get install -y make \
  && apt-get install -y gcc \
  && apt-get install -y tcl
# Install basic redis
RUN wget http://download.redis.io/redis-stable.tar.gz \
    && tar xvsf redis-stable.tar.gz \
    && cd redis-stable \
    && make \
    && make test \
    && make install 
# start local server on docker image 
RUN apt-get install -y python-pip python-dev build-essential
COPY . /code
WORKDIR /code
RUN pip install -Ur requirements.txt
RUN redis-server 
