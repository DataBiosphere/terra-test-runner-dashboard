ARG BASE_CONTAINER=nikolaik/python-nodejs
FROM $BASE_CONTAINER

LABEL maintainer="terra-test-runner-dashboard"

USER pn

RUN mkdir -p /home/pn/apps/dash

# Install requirements.txt
RUN python -m pip install

ADD dash-app.py /home/pn/apps/dash/dash-app.py
ADD . /home/pn/apps/dash/.
