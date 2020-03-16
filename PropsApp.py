#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PropsApp.py
MIT License (c) Marie Faure <dev at faure dot systems>

PropsApp extends MqttApp.
"""

from constants import *
from MqttApp import MqttApp
from MqttVar import MqttVar

import gettext

try:
    gettext.find("PropsApp")
    traduction = gettext.translation('PropsApp', localedir='locale', languages=['fr'])
    traduction.install()
except:
    _ = gettext.gettext  # cool, this hides PyLint warning Undefined name '_'


import os, platform, sys, logging


class PropsApp(MqttApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        self.logger.info(_("Props started"))

        self._last_echo_p = MqttVar('last_echo', str, BLANK_ECHO, logger=self._logger)
        self._publishable.append(self._last_echo_p)

        if self._mqttConnected:
            try:
                (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, "-", qos=MQTT_DEFAULT_QoS, retain=True)
            except Exception as e:
                self._logger.error(
                    "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), "-", MQTT_DISPLAY_TOPIC))
                self._logger.debug(e)

    # __________________________________________________________________
    def onConnect(self, client, userdata, flags, rc):
        # extend as a virtual method
        self.publishMessage(self._mqttOutbox, "MESG " + "echo on")

    # __________________________________________________________________
    def onDisconnect(self, client, userdata, rc):
        # extend as a virtual method
        self.publishMessage(self._mqttOutbox, "MESG " + "echo off")

    # __________________________________________________________________
    def onMessage(self, topic, message):
        # extend as a virtual method
        print(topic, message)
        if message in ["app:startup", "app:quit"]:
            super().onMessage(topic, message)
        elif message.startswith("echo:"):
            text = message[5:]
            self.publishMessage(self._mqttOutbox, "MESG " + "echo: " + text)
            self._last_echo_p.update(text)
            self.publishMessage(self._mqttOutbox, "DONE " + message)
            self.publishDataChanges()
        else:
            self.publishMessage(self._mqttOutbox, "OMIT " + message)

    # __________________________________________________________________
    def publishAllData(self):
        super().publishAllData()

    # __________________________________________________________________
    def publishDataChanges(self):
        super().publishDataChanges()

    # __________________________________________________________________
    def quit(self):
        try:
            self._mqttClient.disconnect()
            self._mqttClient.loop_stop()
        except:
            pass
        self.logger.info(_("Props stopped"))
        sys.exit(0)
