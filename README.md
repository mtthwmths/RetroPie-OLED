# RetroPie-OLED

Show Game Title on 128x64 OLED I2C Display for RetroPie v4.0.2+

## About

I'm going to maintain this as a fork, but most of the original code will be brought into my MathisPi.py file.
My implementation will be only text on the display, so I have removed the image directories from the original.

A big part of this is using custom user-defined runcommand scripts.
This is documented here: https://retropie.org.uk/docs/Runcommand/#runcommand-scripts

## Install

Step 1. Scrape metadata ( https://github.com/RetroPie/RetroPie-Setup/wiki/Scraper )

Step 2. Install Retropie-OLED Script

```shell
cd ~
git clone https://github.com/mtthwmths/RetroPie-OLED.git
cd ./RetroPie-OLED/
chmod 755 install.sh
./install.sh
```
