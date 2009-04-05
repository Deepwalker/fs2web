#!/usr/bin/python

from xmlrpclib import ServerProxy

host = 'localhost'
username = 'freeswitch'
password = 'works'
port = '8080'

server = ServerProxy("http://%s:%s@%s:%s" % (username, password, host, port))
print server.freeswitch.api("show","channels")

