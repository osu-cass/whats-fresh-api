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

This project uses a Vagrant virtual machine to create a homogeneous development
environment and allow developers to destroy and recreate their environment in
the case that something goes horribly, horribly wrong.

To set up this environment on your own machine, you'll need a few things:

**Vagrant**

To install Vagrant, just use your package manager::

    sudo yum install vagrant # Debian or Ubuntu
    sudo apt-get install vagrant # Centos

**vagrant-berkshelf and vagrant-omnibus**

These plugins are used to configure the Vagrant machine. To install these
plugins, you'll need to use Vagrant's plugin manager::

    vagrant plugin install vagrant-berkshelf
    vagrant plugin install vagrant-omnibus

Running the Django project
--------------------------

You're ready to go! To get the environment started, type ``vagrant up`` in the
root of the Git repository.

After a while (this process may take a quite few minutes), your machine will be
ready to use. To log in, type ``vagrant ssh``.

Now you should be on the Vagrant machine::

[vagrant@project-fish ~]$

To get developing, you'll need to prepare your virtual environment. To do so,
first activate the Python virtualenv::

$ source venv/bin/activate

Your prompt should look like this now::

(venv)[vagrant@project-fish ~]$

To install the Python packages needed to run the Django project, run pip with
the ``requirements.txt`` file provided in the root of the repository::

$ pip install -r whats-fresh/requirements.txt

Now, create the database tables using ``manage.py``::

$ python whats-fresh/whats_fresh/manage.py syncdb

You should now be ready to run the Django app!
::
    $ python whats-fresh/whats_fresh/manage.py runserver 0.0.0.0:8000

