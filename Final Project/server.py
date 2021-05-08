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
    stepCount+=100    
    print(stepCount)
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


if __name__ == "__main__":
    x = threading.Thread(target=thread_function, args = ())
    x.start()	
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')
    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)
    while True:
        if(update==1):
            print(str(stepCount))
            client.publish(topic_write, str(stepCount/goal_value))
            update=0
