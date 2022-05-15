# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Matt's comment block.
# Borrowing some of this from github.com/zzeromin/RetroPie-OLED
# Borrowing a LOT of this from Adafruit. 
# "You can't prank someone you don't like. That's just assault." -Mitchell Pritchett

# Here there be imports
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Create the display object
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3c)
# Note you can change the I2C address by passing an i2c_address parameter
# Note you can specify an explicit I2C bus number

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# check if there is already one of these running
#TODO: need to use this pid to kill if greater than 0? need to be sure and NOT 
# get the grep pid also. Right now if it's not running, it would get itself or
# the grep and kill that which will get messy and might cause issues with lock
# files being left...
cmd = "ps -ef | grep mathisPi | awk 'NR==1{printf \"%d\", $2}'"
CurrentPid = int(subprocess.check_output(cmd, shell = True))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
# font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
fontsize = 12
font = ImageFont.truetype('/home/pi/Documents/RobotoMono-VariableFont_wght.ttf', fontsize)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    # These are all modified by MATH04202022
    # IP address - prints IP:<ip-string>
    cmd = "hostname -I | awk '{printf \"IP: %s\",$1}'"
    IP = str(subprocess.check_output(cmd, shell = True ), 'utf-8')[0:16]
    # CPU info usage/ temp - prints CPU:xx.x% x`C
    cmd = "top -bn1 | grep load | awk '{printf \"CPU:%.1f%%\", $(NF-2)}'"
    CPU = str(subprocess.check_output(cmd, shell = True ), 'utf-8')
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    Temp = str(subprocess.check_output(cmd, shell = True ), 'utf-8')
    CpuInfo = str(CPU + " " + Temp)[0:16]
    # MemUsage - prints "Mem:xxxM xx%"
    cmd = "free -m | awk 'NR==2{printf \"Mem:%03d/%3dM%3d%%\", $3,$2,$3*100/$2 }'"
    MemUsage = str(subprocess.check_output(cmd, shell = True ), 'utf-8')[0:16]
    # Disk info xx/xxGB x%
    cmd = "df -h | awk '$NF==\"/\"{printf \"Dsk:%02d/%02dGB %s\", $3,$2,$5}'"
    Disk = str(subprocess.check_output(cmd, shell = True ), 'utf-8')[0:16]
    # date hh:mm dd.mm.yyyy
    cmd = "date '+%H:%M %d.%m.%Y'| awk '{printf \"%s %s\",$1,$2}'"
    Date = str(subprocess.check_output(cmd, shell=True ), 'utf-8')[0:16]
    # Linux Version
    # in the line below -F is used to specify the field separator for awk and can be a regular expression
    cmd = "uname -srmo | awk -F '[-. ]' '{printf \"Ver:%s.%s.%s%s\", $2, $3, $4, $5}'"
    LinVer = str(subprocess.check_output(cmd, shell=True ), 'utf-8')[0:16]
    # Uptime
    cmd = "/usr/bin/cut -d. -f1 /proc/uptime | awk '{printf \"UP4:%03d:%02d:%02d\", $1/86400, $1/3600%24, $1/60%60}'"
    Uptime = str(subprocess.check_output(cmd, shell = True), 'utf-8')[0:16]
    # test string - I needed to know how many characters would fit on the screen.
    Alphabet = "abcdefghijklmnopqrstuvwxyz"

    # need some useful info for emulator
    # current game (or 'emulation station' if no game)maybe follow it with the year in parantheses.
    # can the game be scrolled across like 16 characters?
    # current emulator (gba vs gpsp and such)
    # play-time in current game


    # maybe weather?
    # you could curl it from here: https://api.weather.gov/gridpoints/BMX/86,27/forecast
    # probably need a function to handle parsing the weather json that you get from that request

    # The top yellow is from 0-15
    # blue is from 16-123

    draw.text((x, top), IP, font=font, fill=255)
    draw.text((x, top+15), CpuInfo, font=font, fill=255)
    draw.text((x, top+27), MemUsage, font=font, fill=255)
    draw.text((x, top+39), Disk, font=font, fill=255)
    draw.text((x, top+51), Uptime, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(10)
