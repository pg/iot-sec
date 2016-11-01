# Connect to WiFi network at boot,
# then connect to MQTT Broker

import machine
import ubinascii
import time
import network
from umqtt.simple import MQTTClient
import dht

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {}
dht_sensor = None
client_id = b"esp8266_" + ubinascii.hexlify(machine.unique_id())

def setup_sensor():
    global dht_sensor
    dht_sensor = dht.DHT22(machine.Pin(CONFIG['sensor_pin']))

def setup_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(CONFIG['ssid'], CONFIG['pw'])

def go_to_sleep():
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    #rtc.alarm(rtc.ALARM0, 300000) # Wake after 5 minutes
    rtc.alarm(rtc.ALARM0, 5000) # Wake after 5 seconds
    machine.deepsleep()

def load_config():
    import ujson as json
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json")
        save_config()
    else:
        CONFIG.update(config)
        print("Loaded config from /config.json")

def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")

def main():
    client = MQTTClient(client_id, CONFIG['broker'])
    client.connect()
    print("Connected to {}".format(CONFIG['broker']))
    while True:
        dht_sensor.measure()
        data = '%s,%s' % (dht_sensor.temperature(), dht_sensor.humidity())
        #topic_str = '%s/%s' % (CONFIG['topic'], client_id)
        topic_str = CONFIG['topic']
        client.publish(topic_str,bytes(data, 'utf-8'))
        print('Sensor state: {}'.format(data))
        go_to_sleep()

if __name__ == '__main__':
    load_config()
    setup_sensor()
    setup_wifi()
    main()
