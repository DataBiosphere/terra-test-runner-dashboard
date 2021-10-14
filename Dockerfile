# This Dockerfile has been tested with image tag python3.8-nodejs16 and dependencies frozen in requirements.txt
# The python-nodejs image will need to be in sync and tested with any future upgrades to
# - Python
# - dependencies in requirements.txt (generated by 'pip freeze' command)
ARG BASE_CONTAINER=nikolaik/python-nodejs:python3.8-nodejs16
FROM $BASE_CONTAINER

LABEL maintainer="terra-test-runner-dashboard"

USER pn

RUN mkdir -p /home/pn/apps/testrunner

ADD test_runner_components /home/pn/apps/testrunner/test_runner_components
ADD requirements.txt /home/pn/apps/testrunner/requirements.txt
ADD dashboard.py /home/pn/apps/testrunner/dashboard.py

WORKDIR /home/pn/apps/testrunner

# Install requirements.txt
RUN pip install -r requirements.txt
