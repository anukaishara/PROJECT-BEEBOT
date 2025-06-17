import paho.mqtt.client as mqtt
import json
import time
from threading import Thread

class WifiCommunication:
    def __init__(self, broker="broker.mqttdashboard.com", port=8000):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(
            client_id="Platform_PC_WiFi",
            protocol=mqtt.MQTTv5,
            transport='websockets'
        )
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.received_data = {}
        self.is_connected = False
        
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Connected with result code {rc}")
        self.is_connected = True
        # Subscribe to ESP32 topics
        self.client.subscribe("swarm/esp32/+/data")
    
    def on_message(self, client, userdata, msg):
        try:
            # Parse incoming JSON data from ESP32s
            data = json.loads(msg.payload.decode())
            # Extract ESP32 ID from topic
            esp_id = msg.topic.split('/')[2]
            self.received_data[esp_id] = data
        except Exception as e:
            print(f"Error processing message: {e}")

    def connect(self):
        try:
            self.client.ws_set_options(
                path="/mqtt",
                headers=None
            )
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Connection error: {e}")
            return False
        return True

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.is_connected = False

    def send_data(self, esp_id, data):
        """Send data to specific ESP32"""
        if not self.is_connected:
            return False
        try:
            topic = f"swarm/esp32/{esp_id}/command"
            self.client.publish(topic, json.dumps(data))
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

    def get_latest_data(self):
        """Get the latest data received from all ESP32s"""
        return self.received_data

def wifiAutoSend(shared_data):
    """Function to automatically send data to ESP32s"""
    wifi_com = WifiCommunication()
    if not wifi_com.connect():
        print("Failed to connect to MQTT broker")
        return

    while True:
        try:
            if shared_data[0]:  # Check if there's data to send
                positions_data = shared_data[0]
                # Send position data to each ESP32
                for bot_id, pos_data in positions_data.items():
                    wifi_com.send_data(str(bot_id), {
                        'x': pos_data[0],
                        'y': pos_data[1],
                        'angle': pos_data[2]
                    })
            time.sleep(0.1)  # Small delay to prevent overwhelming the network
        except Exception as e:
            print(f"Error in wifiAutoSend: {e}")
            continue 