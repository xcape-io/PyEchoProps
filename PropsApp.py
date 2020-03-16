#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PropsApp.py
MIT License (c) Marie Faure <dev at faure dot systems>

PropsApp extends MqttApp.
"""

from constants import *
from MqttApp import MqttApp

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
        # display message will '-' for black screen
        if hasattr(self, '_texte'):
            text = self._texte.value
            if not text:
                text = "-"
            try:
                (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, text, qos=MQTT_DEFAULT_QoS, retain=True)
            except Exception as e:
                self._logger.error(
                    "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), text, MQTT_DISPLAY_TOPIC))
                self._logger.debug(e)

    # __________________________________________________________________
    def onMessage(self, topic, message):
        # extend as a virtual method
        print(topic, message)
        if message in ["app:startup", "app:quit"]:
            super().onMessage(topic, message)
        elif message.startswith("afficher:"):
            text = message[9:]
            self._texte.value = text
            if self._mqttConnected:
                try:
                    (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, text, qos=MQTT_DEFAULT_QoS,
                                                             retain=True)
                    self._logger.info(
                        "{0} '{1}' (mid={2}) on {3}".format(_("Program sending message"), message, mid,
                                                            MQTT_DISPLAY_TOPIC))
                except Exception as e:
                    self._logger.error(
                        "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), message,
                                                  MQTT_DISPLAY_TOPIC))
                    self._logger.debug(e)
            self.publishMessage(self._mqttOutbox, "DONE " + message)
            self.publishDataChanges()
            self._sound.play('media/bell.wav')
        elif message.startswith("effacer"):
            self._texte.value = ""
            if self._mqttConnected:
                try:
                    (result, mid) = self._mqttClient.publish(MQTT_DISPLAY_TOPIC, "-", qos=MQTT_DEFAULT_QoS, retain=True)
                    self._logger.info(
                        "{0} '{1}' (mid={2}) on {3}".format(_("Program sending message"), message, mid,
                                                            MQTT_DISPLAY_TOPIC))
                except Exception as e:
                    self._logger.error(
                        "{0} '{1}' on {2}".format(_("MQTT API : failed to call publish() for"), message,
                                                  MQTT_DISPLAY_TOPIC))
                    self._logger.debug(e)
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
