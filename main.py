#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
MIT License (c) Marie Faure <dev at faure dot systems>

Simple MQTT messaging echo props.

To switch MQTT broker, kill the program and start again with new arguments.
Use -d option to start in windowed mode instead of fullscreen.

usage: python3 main.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
 -h, --help   show this help message and exit
 -s SERVER, --server SERVER
      change MQTT server host
 -p PORT, --port PORT change MQTT server port
 -d, --debug   set DEBUG log level
 -l LOGGER, --logger LOGGER
      use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
"""

import paho.mqtt.client as mqtt
import os, sys, platform, signal, uuid
import asyncio

if os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO

from constants import *
from PropsApp import PropsApp
from Singleton import Singleton, SingletonException


me = None
try:
    me = Singleton()
except SingletonException:
    sys.exit(-1)
except BaseException as e:
    print(e)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# translation
import gettext

try:
    gettext.find(APPLICATION)
    traduction = gettext.translation(APPLICATION, localedir='locale', languages=['fr'])
    traduction.install()
except:
    _ = gettext.gettext  # cool, this hides PyLint warning Undefined name '_'

if os.path.isfile('/opt/vc/include/bcm_host.h'):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = PropsApp(sys.argv, mqtt_client, debugging_mqtt=False)

if app._logger:
    app._logger.info(_("Program started"))

loop = asyncio.get_event_loop()

# Assign handler for process exit
signal.signal(signal.SIGTERM, loop.stop)
signal.signal(signal.SIGINT, loop.stop)
if platform.system() != 'Windows':
    signal.signal(signal.SIGHUP, loop.stop)
    signal.signal(signal.SIGQUIT, loop.stop)


# Publish data
async def publishAllData(period):
    while True:
        await asyncio.sleep(period)
        app.publishAllData()


async def publishDataChanges(period):
    while True:
        await asyncio.sleep(period)
        app.publishDataChanges()


loop.create_task(publishAllData(30.0))
loop.create_task(publishDataChanges(3.0))  # usually 3.0 or 1.0 if a process (like mplayer) has no state update period

# May add automation
'''
async def processAutomation(period):
	while True:
		await asyncio.sleep(period)
		app.processAutomation()
loop.create_task(processAutomation(25e-3))
'''

if app._logger:
    if os.path.isfile('/opt/vc/include/bcm_host.h'):
        app._logger.info(_("Program running on Raspberry Pi"))
    elif platform.system() == 'Windows':
        app._logger.info(_("Program running on Windows"))

loop.run_forever()
loop.close()

if os.path.isfile('/opt/vc/include/bcm_host.h'):
    GPIO.cleanup()

try:
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
except:
    pass

if app._logger:
    app._logger.info(_("Program done"))

del (me)

sys.exit(0)
