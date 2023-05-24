import time
import board
import digitalio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import os, ssl, wifi, socketpool

# gets setting from the toml file included
wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))

print("Connected to WIFI")

# MQTT Broker Configuration, gets settings from the toml file included.
MQTT_BROKER = "IP for your broker"
MQTT_PORT = 1883
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# LED pins on the pico W
led_pin = digitalio.DigitalInOut(board.LED)
led_pin.direction = digitalio.Direction.OUTPUT

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Initialize MiniMQTT
mqtt_client = MQTT.MQTT(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    socket_pool=pool,
)

# Used to send messages back to the broker, can be used to send status state etc.
def send_message(message):
    mqtt_client.publish(MQTT_TOPIC, message)

# Callback function for MQTT messages
def on_message(client, topic, message):
    print("Message Recieved:", message)
    # turns on the LED based on message recieved from publisher
    if message == "on":
        led_pin.value = True
    elif message == "off":
        led_pin.value = False

# Module that connects to the broker and subscribes to the topic
def connect_to_mqtt():
    try:
        mqtt_client.connect()
        mqtt_client.subscribe(MQTT_TOPIC)
        mqtt_client.on_message = on_message  # Assign the callback function
        print("Connected to MQTT Broker")
    except Exception as e:
        print("Error connecting to MQTT Broker:", str(e))
        raise



# Main loop that calls the broker connection module and then initilizes the MQTT client.
def main():
    connect_to_mqtt()

    while True:
        try:
            mqtt_client.loop()

        except (ValueError, RuntimeError) as e:
            print("MQTT Client error:", str(e))
            connect_to_mqtt()

        time.sleep(0.1)


# Runs the loop
if __name__ == "__main__":
    main()

