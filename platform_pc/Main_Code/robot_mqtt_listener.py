#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json

ROBOT_ID = "01"  # Change this for each robot
BROKER = "broker.mqttdashboard.com"
PORT = 8000  # Use 1883 for TCP, 8000 for WebSocket

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    # Subscribe to command topic for this robot
    topic = f"swarm/esp32/{ROBOT_ID}/command"
    client.subscribe(topic)
    print("Subscribed to", topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("Received command:", data)
        # Here, you would parse and execute the command on the robot
    except Exception as e:
        print("Error parsing message:", e)

def main():
    client = mqtt.Client(client_id=f"ROBO{ROBOT_ID}", protocol=mqtt.MQTTv5, transport='websockets')
    client.on_connect = on_connect
    client.on_message = on_message

    client.ws_set_options(path="/mqtt")
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main() 