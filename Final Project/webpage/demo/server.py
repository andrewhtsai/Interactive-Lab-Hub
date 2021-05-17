from flask import Flask, Response,render_template
from flask_socketio import SocketIO, send, emit
from subprocess import Popen, call

import time
import json
import socket

import signal
import sys
from queue import Queue

import paho.mqtt.client as mqtt
import uuid
import threading

# the # wildcard means we subscribe to all subtopics of IDD
topic_read = 'IDD/Member_Channel'
topic_write = 'IDD/Goal_Channel'
stepCount = 0
update = 0
goal_value = 10000
# some other examples
# topic = 'IDD/a/fun/topic'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic_read)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
    global stepCount
    global update
	# if (msg.topic == topic_read)
    #if(msg.topic==topic_read):
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
    stepCount+=200    
    #print(stepCount)
    update=1

def thread_function():
	client = mqtt.Client(str(uuid.uuid1()))
	#client = mqtt.Client(str(uuid.uuid1()))

	client.tls_set()

	client.username_pw_set('idd', 'device@theFarm')


	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(
	'farlab.infosci.cornell.edu',
	port=8883)

	client.loop_forever()
	

def thread_function3():
	socketio.run(app, host='0.0.0.0', port=5000)
	

hostname = socket.gethostname()
hardware = 'plughw:3,0'

app = Flask(__name__)
socketio = SocketIO(app)
audio_stream = Popen("/usr/bin/cvlc alsa://"+hardware+" --sout='#transcode{vcodec=none,acodec=mp3,ab=256,channels=2,samplerate=44100,scodec=none}:http{mux=mp3,dst=:8080/}' --no-sout-all --sout-keep", shell=True)


@socketio.on('connect')
def test_connect():
    print('connected')
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('ping-gps')
def handle_message(val):
    emit('pong-gps', stepCount)
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
    x3 = threading.Thread(target=thread_function3, args = ())
    x3.start()	
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')
    client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)
    while True:
        if (update == 1):
            print(str(stepCount))
            client.publish(topic_write, str(stepCount/goal_value))
            update=0
	
