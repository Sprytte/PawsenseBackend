import datetime
import time
import os
import daemon
import requests
import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=6, pd_sck_pin=5)

input("Place known weight onto the scale then press enter")
reading = hx.get_data_mean(readings=100)

known_weight_grams = input("Enter the known weight in grams & press enter")
value = float(known_weight_grams)

ratio = reading / value
print(ratio)
hx.set_scale_ratio(ratio)

path = "/home/henna/Documents/weights.txt"
upload_weight_url = "http://192.168.2.54:5000/upload_weight"
upload_file_url = "http://192.168.2.54:5000/upload_data"


def getWeight():
    weights = []
    try:
        while len(weights) < 10:
            val = hx.get_weight_mean()
            weights.append(val)
        return (sum(weights) / len(weights))
    except Exception:
        GPIO.cleanup()


def log(time, message):
    with open("/home/henna/Documents/logs.txt", 'a') as fh:
        fh.write("{}: {}".format(time, message))


def save_values():
    while True:
        now = datetime.datetime.now()
        if os.path.isfile(path):
            try:
                files = {'data': open(path, 'rt')}
                response = requests.post(upload_file_url, files=files)
                log(now, response)
                os.remove(path)
            except Exception as e:
                with open(path, 'a') as fh:
                    fh.write("time:{}, weight:{}\n".format(now, getWeight()))
                log(now, e)
        else:
            try:
                value = {'time': "{}".format(now), 'weight': getWeight()}
                x = requests.post(upload_weight_url, json=value)
            except Exception as e:
                with open(path, 'a') as fh:
                    fh.write("time:{}, weight:{}\n".format(now, getWeight()))
                log(now, e)

        time.sleep(600)

try:
    with daemon.DaemonContext():
        save_values()
except Exception as e:
    log(datetime.datetime.now(), e)
    GPIO.cleanup()
