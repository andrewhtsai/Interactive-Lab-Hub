import eventlet
eventlet.monkey_patch()

from flask import Flask, Response,render_template
from flask_socketio import SocketIO, send, emit
from subprocess import Popen, call

import time
import json
import socket

import signal
import sys
from queue import Queue
import threading

import paho.mqtt.client as mqtt
import uuid

topic_image = 'IDD/Manhunt'
topic_mpu = 'IDD/MPU'

mpu_data = tuple()

def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic_image)
	client.subscribe(topic_mpu)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

def on_message(cleint, userdata, msg):
	global mpu_data
	if (msg.topic == topic_image):
		f = open("static/received.jpg", "wb") 
		f.write(msg.payload)
		f.close()
	if (msg.topic == topic_mpu):
		mpu_data = eval(msg.payload)
		
	#print(f"topic: {msg.topic} msg: {msg.payload}")
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing

def thread_function():
	client = mqtt.Client(str(uuid.uuid1()))
	client = mqtt.Client(str(uuid.uuid1()))

	client.tls_set()

	client.username_pw_set('idd', 'device@theFarm')


	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(
	'farlab.infosci.cornell.edu',
	port=8883)

	client.loop_forever()


hostname = socket.gethostname()
hardware = 'plughw:2,0'

app = Flask(__name__)
socketio = SocketIO(app)
audio_stream = Popen("/usr/bin/cvlc alsa://"+hardware+" --sout='#transcode{vcodec=none,acodec=mp3,ab=256,channels=2,samplerate=44100,scodec=none}:http{mux=mp3,dst=:8080/}' --no-sout-all --sout-keep", shell=True)


@socketio.on('connect')
def test_connect():
    print('connected')
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('ping-gps')
def handle_message(val):
    emit('pong-gps', mpu_data)
    #print(mpu.acceleration) 



@app.route('/')
def index():
    return render_template('index.html', hostname=hostname)

def signal_handler(sig, frame):
    print('Closing Gracefully')
    audio_stream.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
	x = threading.Thread(target=thread_function, args = ())
	x.start()	
	socketio.run(app, host='0.0.0.0', port=5000)



