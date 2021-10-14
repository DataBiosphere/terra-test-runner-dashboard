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

# Get around some breaking issue with installing latest version of google-cloud-bigquery from requirements.txt.
RUN pip install google-cloud-bigquery==2.28.1

