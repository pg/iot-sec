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
import pytz
import paho.mqtt.client as mqtt
from model import Device, DeviceData

DEBUG = False

class HubClient(object):
    def __init__(self, id, broker_host, broker_port):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_message = self.on_message
        self.mqttc.on_log = self.on_log

        self.mqttc.connect(broker_host, broker_port, 60)
        self.mqttc.subscribe("hub", 0)

        self._hub_id = hub_id
        self.mqttc.subscribe("hub/" + self._hub_id, 0)

        # Re-establish connections to existing devices
        for device in Device.objects:
            self.mqttc.subscribe("device/" + device.id, 0)

        self.mqttc.publish("device/timesync", int((datetime.now(pytz.timezone('US/Eastern')) - datetime(1970, 1, 1, tzinfo=pytz.timezone('US/Eastern'))).total_seconds() * 1000))


    def on_connect(self, mqttc, obj, flags, rc):
        print("Connected to %s:%s" % (mqttc._host, mqttc._port))


    def on_message(self, mqttc, obj, msg):
        # Filter incoming messages
        topic_list = msg.topic.split('/', maxsplit=1)
        if topic[0] is "hub":
            HubMessaging.handle(msg)
        return


    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))


    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))


    def on_log(self, mqttc, obj, level, string):
        if DEBUG:
            print(string)


    def run(self):
        rc = 0
        while rc == 0:
            rc = self.mqttc.loop()


if __name__ == "__main__":
    comms = Comms("/home/pi/sessions/data")
    logg.run()
