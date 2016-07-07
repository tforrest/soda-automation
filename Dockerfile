# Base image
FROM ubuntu:latest

# get dependencies
RUN apt-get update \
  && apt-get install -y python-pip python-dev build-essential

COPY . /src
WORKDIR /src

RUN pip install -Ur requirements.txt
CMD [". env.sh"]
