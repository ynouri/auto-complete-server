# Debian Slim Jessie is a good features/size trade-off
FROM python:3.6

# Workdir
ADD . /auto-complete-docker
WORKDIR /auto-complete-docker

# Dependencies for Tornado & Datrie
#RUN apt-get update
#RUN apt-get install build-essential python-dev

# Instal app & deps
RUN python setup.py install

# Run app
CMD ["python", "-m", "auto_complete_server.web.app"]
