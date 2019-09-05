FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /recp
WORKDIR /recp
ADD . /recp/
RUN rm /recp/apicbase/settings.py && mv /recp/apicbase/settings_docker.py /recp/apicbase/settings.py
RUN sudo apt install pipenv
RUN pipenv install