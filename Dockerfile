ARG BASE_CONTAINER=nikolaik/python-nodejs
FROM $BASE_CONTAINER

LABEL maintainer="terra-test-runner-dashboard"

USER pn

RUN mkdir -p /home/pn/apps/testrunner

ADD requirements.txt /home/pn/apps/testrunner/requirements.txt
ADD dashboard.py /home/pn/apps/testrunner/dashboard.py

WORKDIR /home/pn/apps/testrunner

# Install requirements.txt
RUN pip install -r requirements.txt

