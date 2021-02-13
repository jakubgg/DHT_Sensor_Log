# Sensorlog

Sensorlog is a simple script to read DHT-22 temperature and humidity sensor on your Raspberry Pi and output the results to the terminal/OLED screen/CSV file.

## Prerequisites
You need at least RPi and DHT-22 or compatible sensor. (This setup was tested with RPi0w and RPi 3, but should work with any other version).

You need RaspiOS (or Raspbian) with Python 3.5 or newer (which is usually installed by default).  

For OLED output you need an OLED screen compatible with [Luma.OLED](https://github.com/rm-hull/luma.oled) library (any of SSD1306 / SSD1309 / SSD1322 / SSD1325 / SSD1327 / SSD1331 / SSD1351 / SSD1362 / SH1106). 
By default it uses SSD1306 128x64 screen. If you have screen with different size you might need to adjust "OLED output" section to match your setup.
For displaying text on the screen the script is using `Ubuntu-Mono-Regular` font. You are welcome to change it to whatever you have/need. 

For terminal output you need terminal (duh!).

For specific installation instructions please refer to:
DHT-22 library: (https://github.com/adafruit/Adafruit_Python_DHT)
Luma.OLED library: (https://luma-oled.readthedocs.io/en/latest/install.html)

## Installation

Download `sensorlog.py` file to your RPi home folder (or any other folder when you would like to run this script). 
The script is ready to be run without preceding it with `python3` but in order to do that you have to add `execute` rights to the file. 

```bash
chmod +x ./sensorlog.py
```

but if you'd rather not, that's also fine.

If you use OLED screen and do not have the `Ubuntu` font family installed, you have to download it and unzip it in the folder of your choice. If you choose non-standard folder you have to adjust script with the path to your font file. 

Default fonts installation:

In your home directory (assuming that you are using default `pi` user) create `.fonts` directory

```bash
mkdir ~/.fonts
```

navigate to the `.fonts` directory and download `Ubuntu` font family there

```bash
wget https://assets.ubuntu.com/v1/0cef8205-ubuntu-font-family-0.83.zip
```

unzip only the font we need

```bash
unzip -j ./0cef8205-ubuntu-font-family-0.83.zip ubuntu-font-family-0.83/Ubuntu-R.ttf
```

you can remove now the zip file with the rest of the fonts if you don't need it. 



## Usage

If you added `execute` rights to the script you can run it by simply invoking its name

```bash
sensorlog.py
```

If you prefer to run it with python interpreter and no `execute` rights, then start it via

```bash
python3 sensorlog.py
```

This should run the script in a simple mode and output the DHT sensor readings to the terminal. 

for the full list of options please run 

```bash
sensorlog.py -h
```

The script will run until you hit the `ctrl-c` or the RPi gives up a ghost. 

# Todo

- conversion to F degrees
- split script to only load relevant libraries when requested by cli options
- make it work with default ugly fonts 
- add support for E-Ink screens 
- add parameter for OLED brightness
- add rotating OLED through parameters
- add section on running the file in the background for long running sessions.
- add reading DHT-11 sensor
- upgrade to the Circuit Python library

## Done
+ add check for prerequisites and output nice info messages

# License
[MIT](https://choosealicense.com/licenses/mit/)