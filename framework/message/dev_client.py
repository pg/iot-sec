#!/usr/bin/python

#
# IoT-Sec Framework - Communications Layer
#
# Copyright (c) 2016 Peter Gebhard <pgeb@seas.upenn.edu>
#
# All rights reserved.
#

import re
import os
import sys
import time
from datetime import datetime
from umqtt.simple import MQTTClient

DEBUG = False

class DevClient(object):
    hubs = {}

    def __init__(self, id, broker_host, broker_port, msg_out_callback):
        self.id = id
        self._msg_out_callback = msg_out_callback
        self.mqttc = MQTTClient(self.id, broker_host, broker_port)
        self.mqttc.set_callback(self._on_message)
        self.mqttc.connect()
        self.mqttc.subscribe("device")
        self.own_topic = "device/" + self.id
        self.mqttc.subscribe(self.own_topic)

        # Connect to hub(s)
        self.mqttc.publish("hub", "hello_hub," + self._id)

    def _on_message(self, topic, msg):
        # Handle incoming messages
        if topic is self.own_topic:
            # Catch reply from hub(s)
            if msg.startswith("hello_device"):
                hubs[msg.split(',')[1]] = True

        self._msg_out_callback(out)

    def send(self, msg):
        if msg.dst is None:
            for hub in hubs.keys():
                self.mqttc.publish("hub/" + hub, msg.payload)
        else:
            self.mqttc.publish("hub/" + msg.dst, msg.payload)

    def check_msg(self):
        self.mqttc.check_msg()


if __name__ == "__main__":
    comms = Comms("/home/pi/sessions/data")
    logg.run()
