# Standard Python 3.6 image
FROM python:3.6

# Workdir
ADD . /auto-complete-docker
WORKDIR /auto-complete-docker

# Instal app & deps
RUN python setup.py install

# Run app
CMD ["python", "-m", "auto_complete_server.web.app"]
