import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


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

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    curhour = int(time.strftime("%H"))
    curmin = int(time.strftime("%M"))
    cursec = int(time.strftime("%S"))
    
    #draw hour bar
    draw.text((0, 0), 'H:', font=font, fill = (235, 52, 94))
    draw.rectangle((24, 0, 24 + 9*curhour, 20), outline=1, fill=(235, 52, 94))
    draw.text((28, 0), str(curhour), font=font, fill = (0, 0, 0))

    #draw minute bar
    draw.text((0, 21), 'M:', font=font, fill = (66, 245, 129))
    draw.rectangle((24, 21, 24 + int(3.4*curmin), 40), outline=1, fill=(66, 245, 129))
    draw.text((28, 21), str(curmin), font=font, fill = (0, 0, 0))
    

    draw.text((0, 41), 'S:', font=font, fill = (245, 239, 66))
    draw.rectangle((24, 41, 24 + int(3.4*cursec), 60), outline=1, fill=(245, 239, 66))
    draw.text((28, 41), str(cursec), font=font, fill = (0, 0, 0))
    
    disp.image(image, rotation)
