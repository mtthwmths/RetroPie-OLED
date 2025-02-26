#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Title        : RetroPie_OLED.py
Author       : zzeromin, losernator and members of Tentacle Team
Creation Date: Nov 13, 2016
Cafe         : http://cafe.naver.com/raspigamer
Thanks to    : smyani, zerocool, GreatKStar and members of Raspigamer Cafe.
Free and open for all to use. But put credit where credit is due.

Reference    :
https://github.com/haven-jeon/piAu_volumio
https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
https://pillow.readthedocs.io/en/stable/

Notice       :
installed package(apt): python3-pip python3-dev python3-smbus i2c-tools
installed package(pip): Pillow, adafruit-circuitpython-ssd1306

This code edited for rpi3 Retropie v4.0.2 and later by zzeromin
"""

import time
import os
import board
import textwrap
import busio
import adafruit_ssd1306

from sys import exit
from subprocess import *
from time import *
from datetime import datetime
from random import randint
from PIL import Image, ImageDraw, ImageFont
from board import SCL, SDA
#from board import SCL, SDA

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
#oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x31)

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def get_ip_address(cmd, cmdeth):
    # ip & date information
    ipaddr = run_cmd(cmd)

    # selection of wlan or eth address
    count = len(ipaddr)
    if count == 0 :
        ipaddr = run_cmd(cmdeth)
    return ipaddr

def get_cpu_temp():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def get_cpu_speed():
    tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    cpu_speed = tempFile.read()
    tempFile.close()
    return float(cpu_speed)/1000

def main():

    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = oled.width
    height = oled.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    padding = 0
    top = padding
    bottom = height-padding

    # Load default font.
    font_system = ImageFont.truetype('/home/pi/RetroPie-OLED/neodgm.ttf', 16)
    font_rom = ImageFont.truetype('/home/pi/RetroPie-OLED/BM-HANNA.ttf', 16)
    fonte_rom = ImageFont.truetype('/home/pi/RetroPie-OLED/lemon.ttf', 10)
    font_msg = ImageFont.truetype('/home/pi/RetroPie-OLED/d2.ttf', 11)

    #get ip address of eth0 connection
    cmdeth = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    #get ip address of wlan0 connection
    cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    #cmd = "ip addr show wlan1 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"

    new_Temp = round(get_cpu_temp(),1)
    #old_Speed = new_Speed = get_cpu_speed()

    while True:
        # try to open the log file, failing that display:
        # (msg1, msg2, cpu_temp, IP)
        try:
            f = open('/tmp/retropie_oled.log', 'r', -1,"utf-8")
            # except FileNotFoundError:
        except IOError:
            try:
                titleimg = Image.open("/home/pi/RetroPie-OLED/maintitle.png").convert('1')
            except IOError:
                ipaddr = get_ip_address(cmd, cmdeth)
                ipaddr = ipaddr.decode('utf-8')
                ipaddr = ipaddr.replace("\n","")
                new_Temp = round(get_cpu_temp(),1)
                info = str( new_Temp ) + chr(0xB0) +"C"

                msg1 = "라즈미니파이"
                msg2 = "라즈겜동 텐타클 팀"

                msg1_size = draw.textsize(msg1, font=font_system)
                msg2_size = draw.textsize(msg2, font=font_msg)

                # 'draw' to the image object so that it can be displayed to the
                # screen.
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text(((width-msg1_size[0])/2, top), msg1, font=font_system, fill=255)
                draw.text(((width-98)/2, top+18), msg2, font=font_msg, fill=255)
                draw.text((96, top+54), info , font=fonte_rom, fill=255)
                draw.text((0, top+54), ipaddr, font=fonte_rom, fill=255)

                oled.image(image)
                oled.show()
                sleep(3)
                #break
                pass
            else:
                rx = randint(0, 4) - 2
                ry = randint(0, 2) - 1
                ipaddr = get_ip_address(cmd, cmdeth)
                ipaddr = ipaddr.decode('utf-8')
                ipaddr = ipaddr.replace("\n","")
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                image.paste(titleimg,(rx,ry))
                draw.text((34+rx, top+54+ry), ipaddr, font=fonte_rom, fill=255)
                oled.image(image)
                oled.show()
                sleep(3)
        else:
            system = f.readline()
            system = system.replace("\n","")
            systemMap = {
                "dosbox":"DOS BOX",
                "arcade":"Arcade Game",
                "fba":"FinalBurn Alpha",
                "gba":"GameBoy Advance",
                "kodi":"KODI",
                "mame-mame4all":"MAME4ALL",
                "mame-advmame":"AdvanceMAME",
                "mame-libretro":"lr-MAME",
                "megadrive":"SEGA Megadrive",
                "genesis":"SEGA Genesis",
                "mastersystem":"SEGA Mastersystem",
                "msx":"MSX",
                "nes":"Famicom",   # Nintendo Entertainment System
                "psp":"PSPortable",    # PlayStation Portable
                "psx":"Playstation",
                "ports":"Ports",
                "snes":"Super Famicom", # Super Nintendo Entertainment System
                "notice":"TURN OFF",
            }
            systemicon = systemMap.get(system, "none")
            if systemicon != "none" :
                icon = Image.open("/home/pi/RetroPie-OLED/system/" + system + ".png").convert('1')
                system = systemicon
            rom = f.readline()
            rom = rom.replace("\n","")
            game = rom
            game_length = len(game)
            romfile = f.readline()
            romfile = romfile.replace("\n","")
            f.close()
            new_Temp = round(get_cpu_temp(),1)
            ipaddr = get_ip_address(cmd, cmdeth)
            ipaddr = ipaddr.decode('utf-8')
            ipaddr = ipaddr.replace("\n","")
            info = str( new_Temp ) + chr(0xB0) +"C"

            if game_length == 0 :
                game = romfile
                game_length = len(game)
            try:
                titleimg = Image.open("/home/pi/RetroPie-OLED/gametitle/" + romfile + ".png").convert('1')
                # except FileNotFoundError:
            except IOError:
                #print "no title image"
                system_size = draw.textsize(system, font=font_system)
                gname = textwrap.wrap(game, width=10)
                rx = randint(0, 4) - 2
                ry = randint(0, 2) - 1

                if game_length > 16:
                    current_h, text_padding = 18, 0
                else :
                    current_h, text_padding = 26, 2
                draw.rectangle((0,0,width,height), outline=0, fill=0 )
                if systemicon != "none" :
                    image.paste(icon,(0+rx,0+ry))
                else :
                    draw.text( ((width-system_size[0])/2+rx, top+ry), system, font=font_system, fill=255 )
                for line in gname:
                    #print "text name display"
                    gname_size = draw.textsize(line, font=font_rom)
                    draw.text(((width - gname_size[0])/2+rx, current_h+ry), line, font=font_rom, fill=255)
                    current_h += gname_size[1] + text_padding
                if system == "TURN OFF":
                    draw.text((96+rx, top+54+ry), info , font=fonte_rom, fill=255)
                    draw.text((0+rx, top+54+ry), ipaddr, font=fonte_rom, fill=255)
                oled.image(image)
                oled.show()
                sleep(3)
                pass
            else:
                rx = randint(0, 4) - 2
                ry = randint(0, 2) - 1
                draw.rectangle((0,0,width,height), outline=0, fill=0 )
                image.paste(titleimg,(0+rx,0+ry))
                if system == "TURN OFF":
                    # draw.text((0+rx, top+44+ry), datetime.now().strftime( "%b %d %H:%M" ), font=fonte_rom, fill=255)
                    draw.text((96+rx, top+54+ry), info , font=fonte_rom, fill=255)
                    draw.text((0+rx, top+54+ry), ipaddr, font=fonte_rom, fill=255)
                oled.image(image)
                oled.show()
                sleep(3)

if __name__ == "__main__":
    import sys

    try:
        main()

    # Catch all other non-exit errors
    except Exception as e:
        sys.stderr.write("Unexpected exception: %s" % e)
        sys.exit(1)

    # Catch the remaining exit errors
    except:
        sys.exit(0)
