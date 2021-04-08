#!/usr/bin/env python3

# General libraries
import os
import time
import argparse

# Temp sensor
import Adafruit_DHT

# Oled screen
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

# Setup CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output-file', default=False,
                    help='File name to save the temp and humidity readings as a CSV file. '
                         'If not provided \'-p\' flag assumed',
                    metavar='FILE_NAME')
parser.add_argument('-i', '--interval', default='60', type=int,
                    help='Interval in seconds to poll the thermometer. Min 2s for DHT22. Default = 60s',
                    metavar='SECONDS')
parser.add_argument('-f', '--flush', default='5', type=int,
                    help='How often flush the readings to disk. Value is in lines of CSV. '
                         'With defaults the data will be flushed to disk every 5 lines, i.e. every 5 min.',
                    metavar='LINES')
parser.add_argument('-fo', '--flush-off', action='store_true',
                    help='If switch present, Flushing will be turned off and Python defaults will be used.')
parser.add_argument('-p', '--print', action='store_true',
                    help='If switch present, or if the Output Filename is empty, the script will output values to the '
                         'console.')
parser.add_argument('-s', '--screen', action='store_true', help='Output to an OLED/E-Ink screen. Off by default.')
parser.add_argument('-t', '--test-requirements', action='store_true',
                    help='Run test to check if all dependencies are present')

args = parser.parse_args()


def test_requirements():
    """ Try importing modules from the list of dependencies to check if any are missing.
    Output results to the console and exit.
    """

    import importlib

    modules = {
        'os': 'System module',
        'time': 'System module. Provides various time-related functions.',
        'argparse': 'How are you even read this info?',
        'Adafruit_DHT': 'DHT sensor library - sensor will not be accesible. See '
                        'https://luma-oled.readthedocs.io/en/latest/install.html for more info.',
        'luma.core': 'Necessary for OLED screen output. See https://luma-oled.readthedocs.io/en/latest/install.html '
                     'for more info.',
        'luma.oled': 'Necessary for OLED screen output. See https://luma-oled.readthedocs.io/en/latest/install.html '
                     'for more info.',
        'PIL': 'Necessary for OLED screen output. See https://luma-oled.readthedocs.io/en/latest/install.html for '
               'more info. '
    }

    for mod_name in modules:
        try:
            importlib.import_module(mod_name)
        except ImportError:
            print('\033[91m[-]\033[0m ' + mod_name + '\033[91m not available \033[0m' + ' - ' + modules[mod_name])
        else:
            print('\033[92m[+]\033[0m ' + mod_name + '\033[92m available \033[0m')
    exit()


if args.test_requirements == True:
    test_requirements()

# Setup temp sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Setup defaults
flush_counter = args.flush
line_counter = 1
interval = args.interval
flush_off = args.flush_off

CSV_PATH = '' if args.output_file == False else args.output_file

SERIAL = i2c(port=1, address=0x3C)
oled_device = ssd1306(SERIAL, rotate=2)
oled_device.contrast(5)

# check what output should be initialised
cli_output = False if args.output_file != False and args.print == False else True
csv_output = False if args.output_file == False else args.output_file
oled_output = False if args.screen == False else True

# Setup CSV output

if csv_output != False:
    try:
        csv_file = open(CSV_PATH, 'a+')
        if os.stat(CSV_PATH).st_size == 0:
            csv_file.write('Date,Time,Temperature,Humidity\r\n')
    except (Exception, SystemExit) as e:
        message = "An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args)
        print(message)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:

        # CSV output
        if csv_output != False:
            csv_file.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'),
                                                                  temperature, humidity))

            # skip manual flushing to disk if user overrides defaults
            if flush_off == False:
                if line_counter >= flush_counter:
                    csv_file.flush()
                    line_counter = 0

                line_counter += 1

        # CLI output
        if cli_output == True:
            print(time.strftime('%Y-%m-%d %H:%M:%S') + '  ' + 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature,
                                                                                                           humidity))

        # OLED output
        if oled_output == True:
            with canvas(oled_device) as draw:
                fnt = ImageFont.truetype("/home/pi/.fonts/UbuntuMono-R.ttf", 16)
                draw.text((3, 5), time.strftime('%a %d   %H:%M'), font=fnt, fill="white")
                draw.text((3, 25), 'Temp:    {0:0.1f}˚C'.format(temperature), font=fnt, fill="white")
                draw.text((3, 40), 'Humidity:{0:0.1f}%'.format(humidity), font=fnt, fill="white")

    else:
        print("Failed to retrieve data from humidity sensor")
        exit()

    time.sleep(interval)
