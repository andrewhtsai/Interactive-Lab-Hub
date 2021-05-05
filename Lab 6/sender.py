import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import uuid
import os
from time import sleep

import board
import busio
import adafruit_mpu6050 
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic_image = "IDD/Manhunt"
topic_mpu = 'IDD/MPU'
counter = 0
while True:
	if (counter == 30):
		os.system('raspistill -w 300 -h 200 -o imgs/finder.jpg')
		f = open("imgs/finder.jpg", "rb")
		fileContent = f.read()
		byteArr = bytearray(fileContent)
		client.publish(topic_image, byteArr)
		counter = 0
	client.publish(topic_mpu, str(mpu.acceleration))
	counter += 1
	sleep(0.5)

	

	#cmd = input('>> topic: IDD/')
	#if ' ' in cmd:
	#	print('sorry white space is a no go for topics')
	#else:
	#	topic = f"IDD/{cmd}"
	#	print(f"now writing to topic {topic}")
	#	print("type new-topic to swich topics")
	#	while True:
	#		val = input(">> message: ")
	#		if val =='new-topic':
	#			break
	#		else:
	#			f = open("imgs/suj2.jpg", "rb")
	#			fileContent = f.read()
	#			byteArr = bytearray(fileContent)
	#			#print(byteArr)
	#			client.publish(topic, byteArr)
	#			#publish.single(topic, byteArr, hostname='farlab.infosci.cornell.edu', port=8883)