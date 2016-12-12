#!/usr/bin/python

#
# IoT-Sec Framework - Communications Layer
#
# Copyright (c) 2016 Peter Gebhard <pgeb@seas.upenn.edu>
#
# All rights reserved.
#

DEBUG = False

class BaseClient(object):
    def __init__(self, id, broker_host, broker_port):
        self._id = id
        self._broker_host = broker_host
        self._broker_port = broker_port
