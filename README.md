# raspberrypipicoW-circuit-python-mqtt
simple code for the pico W that is capable of sending and receiving MQTT messages

This code is to show an alternative to umqtt.simple and micropython that is often used with the pico W.
It is alot simpler to use and easier to steup.
It also shows a very simple way to get your pico W connected to WIFI.
All you need is the adafruit_circuitpython_MiniMQTT library in the lib folder on your pico.
Code controls the pico W's LED but can be used to automate via MQTT anything you can use the pico W for.

I use this with Home assistant to turn my PC on and off, I have the pico connected to a transistor then to the powerswitch pins
which simulates a power-switch button press then use Home assisant as a remote.
