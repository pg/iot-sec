# iot-sec Device class
from mongoengine import *
import datetime

class Device(Document):
    id = StringField(required=True, primary_key=True, unique=True)
    manuf = StringField()
    model = StringField()
    pubkey = BinaryField()
    lastSeen = DateTimeField(default=datetime.datetime.now)