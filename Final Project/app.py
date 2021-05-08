import time
import board
import busio
import adafruit_mpu6050
import adafruit_apds9960.apds9960
import qwiic_button
import math
import json
import socket

import signal
import sys
from queue import Queue
import paho.mqtt.client as mqtt
import uuid
 
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)


accels = [0,0,0,0,0,0,0,0,0,0]
counter = 0
stepCount = 0
toggle = 0

topic_write = 'IDD/Member_Channel'
client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

while(True):
	counter = 0
	init_accel = mpu.acceleration
	for i in range(10):
		if(i==0):
        		accels[i] = math.sqrt(((mpu.acceleration[0]-init_accel[0])**2)+((mpu.acceleration[1]-init_accel[1])**2)+((mpu.acceleration[2]-init_accel[2])**2))
			#accels[i] = math.sqrt((mpu.acceleration-init_accel)**2)
		else:
			accels[i] = accels[i-1]+math.sqrt(((mpu.acceleration[0]-init_accel[0])**2)+((mpu.acceleration[1]-init_accel[1])**2)+((mpu.acceleration[2]-init_accel[2])**2))	
			#accels[i] = accels[i-1]+math.sqrt((mpu.acceleration-init_accel)**2)
	if(accels[9]>40):
		if(toggle==0):
			stepCount+=1
			toggle = 1
			time.sleep(0.2)
			print(stepCount)
		else:
			toggle = 0
			time.sleep(0.2)	
	if(stepCount==20):
		client.publish(topic_write, str(stepCount))
		stepCount=0
            
        


