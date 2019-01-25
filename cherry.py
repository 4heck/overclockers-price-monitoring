"""
WSGI config for conf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

import cherrypy
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

application = get_wsgi_application()

# Mount the application
cherrypy.tree.graft(application, "/")

# Unsubscribe the default server
cherrypy.server.unsubscribe()

# Instantiate a new server object
server = cherrypy._cpserver.Server()

# Configure the server object
server.socket_host = "0.0.0.0"
server.socket_port = 5000
server.socket_timeout = 500
server.thread_pool = 30
server.max_request_body_size = 0

# Subscribe this server
server.subscribe()

cherrypy.engine.start()
cherrypy.engine.block()
