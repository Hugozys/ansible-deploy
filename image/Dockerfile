FROM ubuntu:latest
 RUN apt-get update \
  && apt-get install -y python3-pip python3-dev openssh-client \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

 RUN pip3 install paramiko \
  && pip3 install ansible \
  && pip3 install jmespath

