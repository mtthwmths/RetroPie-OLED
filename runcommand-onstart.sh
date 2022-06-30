#!/usr/bin/env bash
# added and modified by zzeromin, zerocool ( 2016-10-13 )
# special thanks to zerocool
# Reference:
# runcommand of RetroPie:  https://github.com/retropie/retropie-setup/wiki/runcommand
# basic script:  https://retropie.org.uk/forum/topic/3731/solved-variables-with-runcommand-onstart-sh/9
# edit and path: $ sudo nano /opt/retropie/configs/all/runcommand-onstart.sh

# get the system name
system=$1

# get the emulator name
emul=$2

# get the full path filename of the ROM
rom=$3

# rom_bn receives $rom excluding everything from the first char to the last slash '/'
rom_bn="${rom##*/}"

# rom_bn receives $rom excluding everything from the last char to the first dot '.'
#rom_bn="${rom%.*}"

# For English User
# Display Game name to EmulationStation and CLCD from same gamelist.xml
GAMELIST1="/home/pi/RetroPie/roms/${system}/gamelist.xml"
GAMELIST2="/home/pi/.emulationstation/gamelists/${system}/gamelist.xml"

# For 2Byte Language User(Korean, Japanese, etc..)
# Display Game name to EmulationStation from gamelist.xml(Korean Game name)
# Display Game name to CLCD from gamelist_en.xml(English Game name)
#GAMELIST1="/home/pi/RetroPie/roms/${system}/gamelist_en.xml"
#GAMELIST2="/home/pi/.emulationstation/gamelists/${system}/gamelist_en.xml"

# this checks if there is a file matching the name stored in GAMELIST1.
# if there is, it uses the retropie rom directory, and if not it uses the
# emulation station directory (like if you use a usb for rom storage).
if [ -f ${GAMELIST1} ]
then
GAMELIST=${GAMELIST1}
else
GAMELIST=${GAMELIST2}
fi
# best I can tell, this uses grep to pull the two lines for the game
# (filename and name) then 'getline;print' prints the second line (the name) 
# then the next two awks strip the <name> and </name> from that line.
title=`grep -s -w -A1 "${rom_bn}" ${GAMELIST} | awk '{getline;print}' | awk 'BEGIN {FS="<name>"} {print $2}' | 
   awk 'BEGIN {FS="</name>"} {print $1}'`
title="${title%%(*}"
rom_bn="${rom_bn%.*}"
# storing the file in the /tmp directory means it gets deleted daily or on
# reboot. also, the '-e' is necessary so that echo understands that '\n' is a
# new line character when "echoing" into the file.
echo -e "$system\n$title\n$rom_bn" > /tmp/mathisPi.log
