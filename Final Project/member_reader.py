import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

import paho.mqtt.client as mqtt
import uuid

import threading

# the # wildcard means we subscribe to all subtopics of IDD
topic_read = 'IDD/Goal_Channel'
progress = 0
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic_read)
	
def on_message(cleint, userdata, msg):
    global progress
    if (msg.topic == topic_read):
        progress = float(msg.payload.decode('UTF-8'))


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

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
y = top
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

x = threading.Thread(target=thread_function, args = ())
x.start()	
while True:
    display_progress = int(progress * 960)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    curhour = int(time.strftime("%H"))
    curmin = int(time.strftime("%M"))
    cursec = int(time.strftime("%S"))
   
    
    draw.rectangle((0, 0, display_progress, 20), outline=1, fill=(235, 52, 94))
    draw.rectangle((0, 20, display_progress-240, 40), outline=1, fill=(235, 52, 94))
    draw.rectangle((0, 40, display_progress-480, 60), outline=1, fill=(235, 52, 94))
    draw.rectangle((0, 60, display_progress-720, 80), outline=1, fill=(235, 52, 94))
    draw.rectangle((0, 80, display_progress-960, 100), outline=1, fill=(50, 168, 82))
    draw.rectangle((0, 100, display_progress-1200, 120), outline=1, fill=(50, 168, 82))


    draw.text((0, 0), 'Goal Progress:', font=font, fill = (235, 231, 23))


    
    disp.image(image, rotation)
