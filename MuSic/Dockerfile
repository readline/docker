FROM ubuntu:lucid
MAINTAINER Kai Yu, "http://readline.net"

# Replace apt-get source and install wget
ADD sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install wget

# Install genome-music
ADD install.sh /opt/install.sh
RUN sh /opt/install.sh
RUN genome install --yes genome-music
RUN rm /opt/install.sh

