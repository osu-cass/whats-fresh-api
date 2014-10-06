.. _development:

===============
Developer Guide
===============

Project Structure
-----------------

Each Django project consists of two things: a Django project, and one or more
Django apps inside that project. For the What's Fresh API, there is only one
app.

The project is named ``whats_fresh``, and the app ``whats_fresh_api``.

The Git repository contains the Django project as a subdirectory, with related
files -- the Vagrant setup file, the pip requirements file, etc in the root of
the repository as well.

Inside the project folder, ``whats_fresh``, there are another two folders and
a ``manage.py`` file. The ``manage.py`` file is a Django script used to control
the project. To read more about it and its functions, see the `Django documentation`_.

.. _`Django documentation`: https://docs.djangoproject.com/en/1.6/ref/django-admin/

Django stores the project information, including ``settings.py``, inside the
second project folder, ``/path/to/repository/whats_fresh/whats_fresh``. The
app itself is stored in ``/path/to/repository/whats_fresh/whats_fresh_api``.

Issue Tracking
--------------

The bug tracker for the What's Fresh API is at `code.osuosl.org`_, and all bugs and feature
requests for the What's Fresh API should be tracked there. Please create an issue for any
code, documentation or translation you wish to contribute.

.. _`code.osuosl.org`: https://code.osuosl.org/projects/sea-grant-what-s-fresh/

Repository Layout
-----------------

We loosely follow `Git-flow <http://github.com/nvie/gitflow>`_ for managing
repository. Read about the `branching model <http://nvie.com/posts/a-successful-git-branching-model/>`_
and why `you may wish to use it too <http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/>`_.


**master**
    Releases only, this is the main public branch.
**release/<version>**
    A release branch, the current release branch is tagged and merged into master.
**develop**
    Mostly stable development branch. Small changes only. It is acceptable that this branch have bugs, but should remain mostly stable.
**feature/<issue number>**
    New features, these will be merged into develop when complete.

When working on new code, be sure to create a new branch from the appropriate place:

-  **develop** - if this is a new feature
-  **release/<version>** - if this is a bug fix on an existing release

Code Standards
--------------

We follow `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_, "the guide for python style".

Developing
==========

Requirements
------------

This project comes with a Test Kitchen configuration set up to manage and create
a homogeneous development environment and allow developers to destroy and
recreate their environment in the case that something goes horribly, horribly
wrong. It's not necessary to use this environment, but using it will make sure
that your environment is as close to the production environment, and to other
developer's environments, as possible.

To set up a development environment yourself, see :ref:`manualSetup`.

To set up this environment on your own machine, you'll need a few things:

**Chef DK**

The first step of this process is to install the Chef Development Kit. It can
be obtained from `getchef.com <http://downloads.getchef.com/chef-dk/>`_

**Ruby Gems**

In order to install the required gems, you'll need to install the ruby

Kitchen is a Ruby gem. To install it, just use ``gem install``::

    $ chef gem install knife-spork knife-flip knife-solve knife-backup knife-cleanup \
      knife-env-diff foodcritic berkshelf test-kitchen kitchen-vagrant kitchen-openstack

**Vagrant**

To install Vagrant, just use your package manager::

    $ sudo yum install vagrant # Debian or Ubuntu
    $ sudo apt-get install vagrant # Centos

**vagrant-berkshelf and vagrant-omnibus**

These plugins are used to configure the Vagrant machine. To install these
plugins, you'll need to use Vagrant's plugin manager::

    $ vagrant plugin install vagrant-berkshelf

**Berks**

Now, you'll need to update your Berkshelf. This allows your virtual machine to
configure itself::

    $ berks update

You're ready to go! To get the environment started, type ``kitchen converge dev``
in the root of the Git repository.

After a while (this process may take a quite few minutes), your machine will be
ready to use. To log in, type ``kitchen login dev``.

Now you should be on the Vagrant machine::

[vagrant@develop-centos-65 ~]$

To get developing, you'll need to prepare your virtual environment. To do so,
first activate the Python virtualenv::

[vagrant@develop-centos-65 ~]$ source /opt/whats_fresh/shared/env/bin/activate

Your prompt should look like this now::

(env)[vagrant@develop-centos-65 ~]$

It's a good idea to navigate to the project directory now, so that ``manage.py``
functions as expected.

::

    (env)[vagrant@develop-centos-65 ~]$ cd whats_fresh/

.. _manualSetup:

Manually setting up the What's Fresh environment
------------------------------------------------

The What's Fresh API has been developed and tested on Python 2.7, Postgres 9.3.5,
and PostGIS 2.1.3, with GDAL 1.9.2.

**Installing PostGIS and requirements**

To install PostGIS, PostgreSQL, and its requirements, follow the installation
instructions on `PostGIS\'s website <http://postgis.net/install/>`_.

After installing PostGIS and Postgres, you'll need to prepare the database
using the ``psql`` tool::

    $ createdb whats_fresh
    $ psql whats_fresh
    whats_fresh-# CREATE EXTENSION postgis;

You can exit the PSQL prompt by pressing Ctrl+D on your keyboard.

**Getting What's Fresh source code**

After PostGIS is installed, you'll need to use ``git`` to clone the What's
Fresh repository. If you don't have ``git``, install it using your system's
package manager.

Now, clone the API repository::

    $ git clone https://github.com/osu-cass/whats-fresh-api.git

This will place the source code in the subdirectory ``whats-fresh-api``. You'll
want to use a Python virtual environment and the ``pip`` package manager to
set up the Python requirements::

    $ cd whats-fresh-api
    $ virtualenv ~/.virtualenvs/whats-fresh
    $ source ~/.virtualenvs/whats-fresh/bin/activate
    (whats-fresh)$ pip install -r requirements.txt
    $ cd whats_fresh

You're now ready to run and develop the project!

Running the Django project
--------------------------

At this point, you should have a working database and copy of the source code.
You may be developing on your physical machine, or using a virtual machine as
described above. After setting up the virtual environment, change to the
directory with ``manage.py`` inside.

Now, create the database tables using ``manage.py``::

    (env)[vagrant@develop-centos-65 ~]$ python manage.py syncdb

If you plan on loggin into the web interface, you'll need to create a user
account. You can use ``manage.py`` to create a superuser account::

    (env)[vagrant@develop-centos-65 ~]$ python manage.py createsuperuser

You should now be ready to run the Django app!
::

    (env)[vagrant@develop-centos-65 ~]$ python manage.py runserver 0.0.0.0:8000

To access the server in your web browser, navigate to ``http://172.16.16.2:8000``.

Testing
-------

The What's Fresh API uses `test-driven development<http://en.wikipedia.org/wiki/Test-driven_development>`.
What this means is that, before writing a feature -- be it a new API endpoint,
a model, or a bug fix -- you should write a test. After writing the feature,
run the test to verify that it works, and when you're satisfied with your
implementation, re-run the entire test suite to make sure there were no
regressions.

Each test lives inside the ``whats_fresh_api/tests/`` directory, organized into
a subdirectory based on what kind of test it is. For instance, all model tests
live inside the ``models`` subdirectory, while views would live inside the
``view`` directory.

For information on how to write tests, see ``Django's guide on writing tests``<https://docs.djangoproject.com/en/1.6/topics/testing/overview/>``.

Let's say you've just modified the code -- say, you edited the Vendor model
due to a bug you found. Instead of running the entire testing suite, you can
run just one set of tests at a time::

    (env)[vagrant@develop-centos-65 whats_fresh]$ python manage.py test whats_fresh_api.tests.models.test_vendor_model.VendorTestCase

.. note::

    Running tests is based on the directory name, using the following syntax::

        whats_fresh_api.tests.<test subdirectory>.<test file>.<test class name>

    For a test called ImageTestCase inside of ``tests/views/test_image_view.py``,
    you would need to run the following command::

        (env)[vagrant@develop-centos-65 whats_fresh]$ python manage.py test whats_fresh_api.tests.views.test_image_view.ImageTestCase

To make sure that you didn't break anything unexpected, it can be a good idea
to periodically run the entire testing suite::

    (env)[vagrant@develop-centos-65 whats_fresh]$ python manage.py test

**Fixtures**

Django allows you to load pre-written data into the database for testing
purposes. The data is stored in files called fixtures, and for testing
purposes, the What's Fresh API comes with a few hand-written (for running
tests where we need to know the input data) and a large number of automatically
generated (for when we simply want to have data in our database).

To install a fixture, use the ``manage.py`` command's loaddata option::

    (env)[vagrant@develop-centos-65 whats_fresh]$ manage.py loaddata fixtures

The hand-written fixtures are stored in ``fixtures``, and the automatically
generated ones in ``random``.
