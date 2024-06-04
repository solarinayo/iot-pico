import ahtx0
from machine import Pin, I2C
from time import sleep
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = ahtx0.AHT10(i2c)

#taking or capturing temp within the surroundings

while True:
    print("AYo the current temperature is:"  , sensor.temperature, "Humidity:", sensor.relative_humidity)
    sleep(0.5)
