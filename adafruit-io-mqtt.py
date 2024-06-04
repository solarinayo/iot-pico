from machine import Pin, I2C
from time import sleep
import network
import socket
import random
import ahtx0
from umqtt.simple import MQTTClient

# Initialize I2C and sensor
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = ahtx0.AHT10(i2c)


ssid = 'Nordic Hotel Lagos'
password = 'Nordic.21.Oslo'


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Connecting to WiFi...')
        sleep(1)
    print('Connected to WiFi')
    return wlan

wlan = connect_wifi()

# MQTT setup
mqtt_server = 'io.adafruit.com'
mqtt_port = 1883 # non-SSL port
mqtt_user = 'Solarinayo' # Adafruit IO Username
mqtt_password = '#' # Adafruit IO Key
mqtt_topic = 'Solarinayo/feeds/temperature' # Adafruit IO Feed Key
mqtt_client_id = str(random.randint(10000, 999999)) # Must have a unique ID

def mqtt_connect():
    client = MQTTClient(client_id=mqtt_client_id, server=mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password, keepalive=3600)
    client.connect()
    print(f'Connected to {mqtt_server} MQTT Broker')
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

# Main loop
while True:
    if wlan.isconnected():
        temp = sensor.temperature
        humidity = sensor.relative_humidity
        print(f"AYo the current temperature is: {temp} Humidity: {humidity}")
        client.publish(mqtt_topic, str(temp))
    else:
        reconnect()
    sleep(20)

