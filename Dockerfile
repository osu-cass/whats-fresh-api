FROM ubuntu:16.04

MAINTAINER OSU Open Source Lab, support@osuosl.org


ENV PASSWORD whats_fresh
ENV HOST postgis
ENV USER whats_fresh
ENV NAME template_postgis
ENV ENVIRONMENTCONFIG True
ENV ENGINE django.contrib.gis.db.backends.postgis

EXPOSE 8000

# Add UbuntuGIS repository to install GDAL
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends software-properties-common
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get -y update

RUN apt-get install -y --no-install-recommends \
    python-dev \
    python-setuptools \
    python-pip \
    build-essential \
    postgresql-server-dev-9.5 \
    gdal-bin

RUN easy_install pip

WORKDIR /opt/whats_fresh

COPY . /opt/whats_fresh
RUN pip install wheel
RUN pip install .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
