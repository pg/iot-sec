# Connect to WiFi network at boot,
# then connect to MQTT Broker

import machine
import ubinascii
import time
import network
from umqtt.simple import MQTTClient

CONFIG = {}
client_id = b"esp8266_" + ubinascii.hexlify(machine.unique_id())

def setup_sensors():
    global door_sensor
    door_sensor = machine.Pin(CONFIG['door_pin'])
    global pir_sensor
    pir_sensor = machine.Pin(CONFIG['pir_pin'])
    global batt_volt
    batt_volt = machine.ADC(0)

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
        data = '%s,%s,%s' % (pir_sensor.value(), door_sensor.value(), batt_volt.read())
        #topic_str = '%s/%s' % (CONFIG['topic'], client_id)
        topic_str = CONFIG['topic']
        client.publish(topic_str,bytes(data, 'utf-8'))
        print('Sensors states: {}'.format(data))
        #go_to_sleep()

if __name__ == '__main__':
    load_config()
    setup_sensors()
    setup_wifi()
    main()
