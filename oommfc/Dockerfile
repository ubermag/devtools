FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip tk-dev tcl-dev
RUN python3 -m pip install --upgrade pip pytest-cov oommfc

WORKDIR /usr/local/

RUN git clone https://github.com/fangohr/oommf.git

WORKDIR /usr/local/oommf/

RUN make

ENV OOMMFTCL /usr/local/oommf/oommf/oommf.tcl

WORKDIR /usr/local/