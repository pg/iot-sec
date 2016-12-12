# iot-sec Firmware Site class
from mongoengine import *
import datetime

class FirmwareSite(Document):
    id = StringField(required=True, primary_key=True, unique=True)
    manuf = StringField()
    url = StringField()
    # TODO: Associated Devices
    lastChecked = DateTimeField(default=datetime.datetime.now)