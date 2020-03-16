# PyEcho props
***A connected props to echo messages to its sender.***

[PyEcho props](https://github.com/fauresystems/PyEchoProps) is pure python application to build a Raspberry connected props for Escape Room. It can be used as a base example to hack for creating your own props. It is used in the [**Room** plugin tutorial](https://xcape.io/public/documentation/en/room/Plugintutorial.html).

This props listen to MQTT messages received in its inbox and replies the message to its sender.

The props is intended to be controlled from *<a href="https://xcape.io/" target="_blank">xcape.io</a>* **Room** software, see <a href="https://xcape.io/public/documentation/en/room/AddaRaspberrypropsTeletext.html" target="_blank">Add a Raspberry props in the Room manual</a>.


## Installation
Download `PyEchoProps-master.zip` from this GitHub repository and unflate it on your Raspberry Pi.

Install dependencies
```bash
pip3 install -r requirements.txt
```

Edit `definitions.ini` to set MQTT topics for your Escape Room:
```python
[mqtt]
; mqtt-sub-* and app-inbox topics are subscribed by MqttApp
app-inbox = Room/My room/Props/Raspberry Echo/inbox
app-outbox = Room/My room/Props/Raspberry Echo/outbox
mqtt-sub-room-scenario = Room/My room/Control/game:scenario
``` 


## Usage
Start `main.py` script:

```bash
usage: python3 main.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
 -h, --help   show this help message and exit
 -s SERVER, --server SERVER
      change MQTT server host
 -p PORT, --port PORT change MQTT server port
 -d, --debug   set DEBUG log level
 -l LOGGER, --logger LOGGER
      use logging config file
```

To switch MQTT broker, kill the program and start again with new arguments.


## SSH relaunch commande
The command to relaunch the props from *<a href="https://xcape.io/" target="_blank">xcape.io</a>* **Room** software is :

```bash
$ ps aux | grep python | grep -v "grep python" | grep PyEchoProps/main.py | awk '{print $2}' | xargs kill -9 && screen -d -m python3 /home/pi/Room/Props/PyEchoProps/main.py -s %BROKER%
```


## Understanding the code

### *PropsApp*
Echo props is built with the following files:
* `main.py` main script to start the props
* `constants.py`
* `definitions.ini`
* `logging.ini`
* __`PropsApp.py`__ props related code

It depends on:
* `MqttApp.py` base class to publish/subscribe MQTT messages
* `MqttVar.ini` base class to optimize network communications
* `Singleton.ini` to ensure one instance of application is running

You can use __`PropsApp.py`__ as a template to create your own connected props, you will also add GPIO elements.

About `create-props-tgz.bat`:
* install <a href="https://www.7-zip.org/" target="_blank">7-Zip</a> on your Windows desktop
* run `create-props-tgz.bat` to archive versions of your work

#### MQTT message protocol:
> This props has been created to be controlled with **Room** software so MQTT messages published in the props outbox implement the [Room Outbox protocol](PROTOCOL.md).

#### IDE for hacking `EchoApp.py`:
> You can open a PyCharm Professional project to hack the code remotely, thanks to `.idea` folder. Or if you prefer to the code hack directly on the Raspberry, we suggest <a href="https://eric-ide.python-projects.org/" target="_blank">Eric6 IDE</a>. 


### *MqttApp* and *MqttVar* base classes
*PropsApp* extends *MqttApp*, the python base app for Raspberry connected props.

MQTT topics are defined in *definitions.ini*.

***PubSub*** variables extend *MqttVar*, it is an helper to track value changes and to optimize publishing values in MQTT topic outbox.

You might not modify `MqttApp.py` an `MqttVar.py` files.

#### Notes about MQTT QoS:
>*Python script hangs* have been reported when `paho-mqtt` is running asynchronously with QoS 2 on a network with significant packet loss (particularly Wifi networks).

We have choosen MQTT QoS 1 as default (see *constants.py*).


## Other python frameworks for connected props
At <a href="https://faure.systems/" target="_blank">Faure Systems</a> we engineered connected props with several frameworks for many different needs:

* *Asyncio* props
    - game automation
    - relay box control (room electricity and doors)
    - GPIO only automation
* *PyGame* props
    - Tetris hacked
    - mechanic Piano sound player
    - hacker intrusion puzzle
* *PyQt5* props
    - fortune telling table (alphanum LED switching)
    - electric jack cylinder control
* *Guizero* props
    - teletext
* *Kivy* props
    - teletext with visual effects
    
You may follow on our <a href="https://github.com/fauresystems?tab=repositories" target="_blank">GitHub repositories</a>, props source code is planned to be published in year 2020.


## Author

**Marie FAURE** (Oct 9th, 2019)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>