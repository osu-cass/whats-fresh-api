What's Fresh API
================

The API component of the What's Fresh project.

Setting up Developer Environment
================================

This project uses a Vagrant virtual machine to create a homogeneous development
environment and allow developers to destroy and recreate their environment in
the case that something goes horribly, horribly wrong.

To set up this environment on your own machine, you'll need a few things:

1. Vagrant

To install Vagrant, just use your package manager:

``sudo yum install vagrant``

``sudo apt-get install vagrant``

2. ``vagrant-berkshelf`` and ``vagrant-omnibus``

These plugins are used to configure the Vagrant machine. To install these
plugins, you'll need to use Vagrant's plugin manager:

``vagrant plugin install vagrant-berkshelf``

``vagrant plugin install vagrant-omnibus``

-------------------------

You're ready to go! To get the environment started, type ``vagrant up`` in the
root of the Git repository.

After a while (this process may take a quite few minutes), your machine will be
ready to use. To log in, type ``vagrant ssh``.

Now you should be on the Vagrant machine::

``[vagrant@project-fish ~]$``

To get developing, you'll need to prepare your virtual environment. To do so,
first activate the Python virtualenv::

``$ source venv/bin/activate``

Your prompt should look like this now::

``(venv)[vagrant@project-fish ~]$``

To install the Python packages needed to run the Django project, run pip with
the ``requirements.txt`` file provided in the root of the repository:

``$ pip install -r whats-fresh/requirements.txt``

You should now be ready to run the Django app!

``$ python whats-fresh/project_fish/manage.py runserver 0.0.0.0:8000``

