# iot-sec Device Data class
from mongoengine import *
import datetime

class DeviceData(Document):
    id = ObjectIdField(required=True, unique=True)
    device = StringField(required=True, primary_key=True)
    data = StringField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.now, required=True)