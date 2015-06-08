FROM ubuntu:trusty
MAINTAINER Kai Yu, "http://readline.net"

# Install required softwares
ADD install.sh /opt/install.sh
RUN sh /opt/install.sh
ADD dbPrepare.sh /opt/dbPrepare.sh
ADD blastdbPrepare.sh /opt/blastdbPrepare.sh

ENV PYTHONPATH /opt/kobas2.0-20150126/src:$PYTHONPATH
ENV PATH /opt/kobas2.0-20150126/scripts:$PATH
ENV LD_LIBRARY_PATH /usr/local/lib/R/lib:$LD_LIBRARY_PATH
