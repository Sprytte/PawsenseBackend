import datetime
import time
import os
import daemon
import requests
import RPi.GPIO as GPIO
from hx711 import HX711

#Script in the raspberry pi
#Setting up
GPIO.setmode(GPIO.BCM)
hx = HX711(dout_pin=6, pd_sck_pin=5)

path = "/home/henna/Documents/weights.txt"
upload_weight_url = "http://192.168.2.54:5000/upload_weight"
upload_file_url = "http://192.168.2.54:5000/upload_data"

#Calibrating
input("Place known weight onto the scale then press enter")
reading = hx.get_data_mean(readings=100)

known_weight_grams = input("Enter the known weight in grams & press enter")
value = float(known_weight_grams)

#Getting ratio
ratio = reading / value
print(ratio)
hx.set_scale_ratio(ratio)

def getWeight():
    weights = []
    try:
        #collect 10 readings and get the average for more accurate results
        while len(weights) < 10:
            val = hx.get_weight_mean()
            weights.append(val)
        return (sum(weights) / len(weights))
    except Exception:
        GPIO.cleanup()

#logs for debugging purposes
def log(time, message):
    with open("/home/henna/Documents/logs.txt", 'a') as fh:
        fh.write("{}: {}".format(time, message))


def save_values():
    while True:
        now = datetime.datetime.now()
        #if data was saved on local file
        if os.path.isfile(path):
            try:
                #upload
                files = {'data': open(path, 'rt')}
                response = requests.post(upload_file_url, files=files)
                log(now, response)
                os.remove(path)
            except Exception as e:
                #save the reading in the file
                with open(path, 'a') as fh:
                    fh.write("time:{}, weight:{}\n".format(now, getWeight()))
                log(now, e)
        else:
            try:
                #send the reading to the flask server
                value = {'time': "{}".format(now), 'weight': getWeight()}
                x = requests.post(upload_weight_url, json=value)
            except Exception as e:
                #if unsuccessful, save it to local file
                with open(path, 'a') as fh:
                    fh.write("time:{}, weight:{}\n".format(now, getWeight()))
                log(now, e)
                
        #do this every 10 minutes
        time.sleep(600)

try:
    with daemon.DaemonContext():
        save_values()
except Exception as e:
    log(datetime.datetime.now(), e)
    GPIO.cleanup()
