# pull official base image
FROM python:3.8.6

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#ENV DIR1=P13-CheckListMgr
ENV DIR1=./
ENV DIR2=checklistmgr

# install dependencies
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# set work directory
WORKDIR /home/jmlm

# create and activate virtual environment
RUN python3 -m venv env

# copy and install pip requirements
RUN ./env/bin/pip3 install --upgrade pip setuptools
COPY ./${DIR1}/requirements.txt /home/jmlm/requirements/requirements.txt
RUN ./env/bin/python3 -m pip install --upgrade pip
RUN ./env/bin/pip3 install wheel
RUN ./env/bin/pip3 install -r /home/jmlm/requirements/requirements.txt

# copy Django project files
COPY ./${DIR1}/${DIR2}/ /home/jmlm/${DIR2}
WORKDIR /home/jmlm/${DIR2}

# create django-log dir
RUN mkdir -m 766 /var/log/django

EXPOSE 8000 

# Command
# CMD /home/jmlm/env/bin/gunicorn --workers 3 --access-logfile - --bind 0.0.0.0:8000 checklistmgr.wsgi:application


