FROM centos:7

MAINTAINER OSU Open Source Lab <support@osuosl.org>


ENV USERNAME whats_fresh
ENV PASSWORD whats_fresh
ENV DBNAME whats_fresh
ENV HOST postgis
ENV USER whats_fresh
ENV NAME  whats_fresh
ENV ENVIRONMENTCONFIG True
ENV ENGINE django.contrib.gis.db.backends.postgis
ENV CONTAINERPORT 5432
ENV HOSTPORT 5432

RUN yum install -y python-devel python-setuptools postgresql-devel gcc curl

# Install the ius repository to install GDAL
RUN curl http://dl.iuscommunity.org/pub/ius/stable/CentOS/7/x86_64/ius-release-1.0-13.ius.centos7.noarch.rpm > /tmp/ius.rpm
RUN yum install -y /tmp/ius.rpm
RUN yum install -y gdal

RUN easy_install pip

WORKDIR /opt/whats_fresh

COPY . /opt/whats_fresh
RUN pip install .
CMD ["python", "manage.py", "runserver", "postgis:8000"]
