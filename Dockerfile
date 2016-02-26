FROM centos:7

MAINTAINER OSU Open Source Lab, support@osuosl.org


ENV PASSWORD whats_fresh
ENV HOST postgis
ENV USER whats_fresh
ENV NAME  template_postgis
ENV ENVIRONMENTCONFIG True
ENV ENGINE django.contrib.gis.db.backends.postgis

EXPOSE 8000

RUN yum install -y python-devel python-setuptools postgresql-devel gcc curl

# Install the ius repository to install GDAL
RUN curl http://dl.iuscommunity.org/pub/ius/stable/CentOS/7/x86_64/ius-release-1.0-14.ius.centos7.noarch.rpm > /tmp/ius.rpm
RUN yum install -y /tmp/ius.rpm
RUN yum install -y gdal

RUN easy_install pip

WORKDIR /opt/whats_fresh

COPY . /opt/whats_fresh
RUN pip install .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
