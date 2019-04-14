import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
import paho.mqtt.client as paho
import time
import subprocess 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect("broker.mqttdashboard.com", 1883)
client.loop_start()
GPIO.setup(27,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(17,GPIO.IN,pull_up_down = GPIO.PUD_UP)
port = serial.Serial("/dev/ttyAMA0",baudrate=9600,timeout=0.5)
B1_lt = 12.9527139
B1_ln = 80.14226

B2_lt = 0
B2_ln = 0

B3_lt = 0
B3_ln = 0
while True:
    subprocess.call(['sudo','python','gps.py','For Location Tracking'])
    if(GPIO.input(17) == 1):
	print('Sending meaage')
	subprocess.call(['sudo','python','sms.py','Alert storm is comming'])
    
    if(GPIO.input(27) == 1):
	print('Sending Buzzer to boat')
	port.write('A')
    elif(GPIO.input(27) == 0):
	port.write('a')
    rcv = port.readline()
    if(len(rcv)>1):
	data = rcv.split(' ')
	lat = float(data[0].split(':')[1])
	lng = float(data[1].split(':')[1])
	print lat,lng
	if((abs(B1_lt - lat)<0.001)and(abs(B1_ln - lng)<0.001)):
		print('crossed border1')
		client.publish("marine/srilankaboat", 'crossed border1', qos=1)
		subprocess.call(['sudo','python','sms.py',lat+lng])
	if((abs(B2_lt - lat)<0.001)and(abs(B2_ln - lng)<0.001)):
		print('crossed border2')
		client.publish("marine/srilankaboat", 'crossed border2', qos=1)
		subprocess.call(['sudo','python','sms.py',lat+lng])
	if((abs(B3_lt - lat)<0.001)and(abs(B3_ln - lng)<0.001)):
		print('crossed border3')
		client.publish("marine/srilankaboat", 'crossed border3', qos=1)
		subprocess.call(['sudo','python','sms.py',lat+lng])
