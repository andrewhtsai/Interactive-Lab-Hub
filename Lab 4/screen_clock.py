import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import busio

import adafruit_mpr121
import adafruit_mpu6050
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
mpu = adafruit_mpu6050.MPU6050(i2c)



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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

yScroll = 0
accelArray = [0.0, 0.0, 0.0, 0.0, 0.0]
avgArray = [0.0, 0.0, 0.0]
timeCount = 0
while True:
    posArray = [(0,(0 + yScroll)), (0,(66 + yScroll)), (0,(132 + yScroll)), (0,(198 + yScroll))]
    instArray = ["5oz Tequila", "4oz Lime Juice", "3oz Triple-Sec", "Add Ice, Shake"]
    fillArray = [(235, 52, 94), (66, 245, 129), (245, 239, 66), (255, 255, 255)]

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    draw.text(posArray[0], instArray[0], font=font, fill = fillArray[0])

    draw.text(posArray[1], instArray[1], font=font, fill = fillArray[1])
    
    draw.text(posArray[2], instArray[2], font=font, fill = fillArray[2])

    draw.text(posArray[3], instArray[3], font=font, fill = fillArray[3])
    
    if(yScroll<-195):
        accelArray[0:3] = accelArray[1:4]
        accelArray[4] = (abs(mpu.acceleration[0])+abs(mpu.acceleration[1]+9.8)+abs(mpu.acceleration[2]))*(abs(mpu.acceleration[0])+abs(mpu.acceleration[1]+9.8)+abs(mpu.acceleration[2]))
        avgArray[0:1] = avgArray[1:2]
        avgArray[2] = (accelArray[0]+accelArray[1]+accelArray[2]+accelArray[3]+accelArray[4])
        if((avgArray[0]+avgArray[1]+avgArray[2])/3)>10:
            draw.text((0, 33), "Good!", font=font, fill = (0,255,0))
        else:
            draw.text((0, 33), "Faster", font=font, fill = (255,0,0))
        draw.rectangle((0, 66, 6*timeCount, 99), outline=1, fill=(0,255,0))
        #print(6*timeCount)
        timeCount+=1
        if(timeCount>=40): 
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((0, 0), "DONE!", font=font, fill = (0,255,0))
        time.sleep(0.25)
        
    else:
        for i in range(2):
            if mpr121[i*5].value:
                if(i==0): yScroll+=3
                if(i==1): yScroll-=3
        curtime = time.time
    disp.image(image, rotation)
    #print((avgArray[0]+avgArray[1]+avgArray[2])/3)
    #yScroll = yScroll%135

