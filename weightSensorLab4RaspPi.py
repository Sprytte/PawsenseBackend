import datetime
import time
import daemon
import requests
import RPi.GPIO as GPIO
from hx711 import HX711

#Setting board and sensor pins
GPIO.setmode(GPIO.BCM)
hx = HX711(dout_pin=6, pd_sck_pin=5)

#Calibrating weight sensor
input("Place known weight onto the scale then press enter")
reading = hx.get_data_mean(readings=100)

known_weight_grams = input("Enter the known weight in grams & press enter")
value = float(known_weight_grams)

ratio = reading / value
print(ratio)
hx.set_scale_ratio(ratio)

#Constants to upload weight data
data_file = "/home/henna/Documents/weights.txt" #Saving file onto raspberrypi
upload_url = "http://192.168.2.54:5000/upload_data"
now = datetime.datetime.now()
request_time = now.replace(hour=19, minute=37, second=0, microsecond=0) #Time I want file to be uploaded

#Function to read weight from sensor
def getWeight():
    weights = []
    try:
        while len(weights) < 10: #Collecting weight 10 times and get average for more accuracy
            val = hx.get_weight_mean()
            weights.append(val)
        return (sum(weights) / len(weights))
    except Exception:
        GPIO.cleanup()


#Function to run in daemon
def save_values():
    while True:
        with open('/home/henna/Documents/weights.txt', 'a') as fh: #Save weight data
            fh.write("time:{}, weight:{}\n".format(datetime.datetime.now(), getWeight()))

        #Upload file at time set
        if(now >= (request_time - datetime.timedelta(hours=0, minutes=3)) or now <= (request_time + datetime.timedelta(hours=0, minutes=3))):
            try:
                files = {'data': open(data_file, 'rt')}
                response = requests.post(upload_url, files=files)
            except Exception as e:
                with open('/home/henna/Documents/weights.txt', 'a') as fh: #Write an error message if it fails
                    fh.write("time:{}, REQUEST UNSUCCESSFUL {}\n".format(now, e))

        time.sleep(300) #Collect data every 5 minutes


try:
    with daemon.DaemonContext():
        save_values()
except Exception:
    GPIO.cleanup()
