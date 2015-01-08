FROM centos:7

MAINTAINER OSU Open Source Lab <support@osuosl.org>

RUN yum install -y python-devel python-setuptools postgresql-devel gcc
RUN easy_install pip

WORKDIR /opt/whats_fresh
COPY . /opt/whats_fresh
RUN pip install .

CMD ["python", "manage.py", "runserver"]
