Deployment
==========

As Pyroutes is a WSGI-based framework, we have several methods of deploying our
applications. The most common is to use mod_wsgi and Apache.


Apache2.2 and mod_wsgi
----------------------

As this web framework is based on WSGI, we'll use mod_wsgi as our way of
deploying our project behind the Apache webserver.

Let's start by setting up our base requirements (assuming you have pyroutes installed).

**Debian based systems**::

    sudo aptitude install apache2 libapache2-modwsgi
    sudo a2enmod wsgi
    sudo /etc/init.d/apache2 reload

**Other**

- Install apache from www.apache.com
- Install mod_wsgi from http://code.google.com/p/modwsgi
- Enable mod_wsgi and restart apache (might be different on your platform)::

    sudo a2enmod wsgi
    sudo apache2ctl restart


Once you have that installed we're going to need a ``VirtualHost`` for our project.
Use this configuration as an example. More configuration options are available at mod_wsgi's website.::

    <VirtualHost *>
            ServerName example.pyroutes.com
            ServerAdmin klette@pyroutes.com
            DocumentRoot /home/klette/dev/myproject/webroot

            WSGIScriptAlias / /home/klette/dev/myproject/handler.py
    </VirtualHost>

The most important line here is the ``WSGIScriptAlias`` line. In the example we declare that every path under ``/`` should
be handled by that python file. When using ``pyroutes`` this is the file where you do::

  from pyroutes import application

and import all files and modules declaring routes.

If ``WSGIScriptAlias`` is set to a different path, e.g. ``/projects/wiki``,
Redirect responses starting with a slash are made relative to this path.

That should be about it, and your project should be running smoothly behind apache.
