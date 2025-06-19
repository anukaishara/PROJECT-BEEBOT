#!/usr/bin/env python3
"""
Test script to demonstrate sending JSON motor commands via MQTT
This replaces the protobuf-based communication with JSON format
"""

import paho.mqtt.client as mqtt
import json
import time
import sys

# MQTT Configuration
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC_PREFIX = "swarm/esp32"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        print("Successfully connected to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")

def on_message(client, userdata, msg):
    """Handle incoming messages from ESP32s"""
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        print(f"Received from {msg.topic}: {data}")
    except json.JSONDecodeError:
        print(f"Received non-JSON message: {msg.payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

def send_motor_command(client, robot_id, start_angle, distance, end_angle):
    """Send a motor command in JSON format"""
    command = {
        "id": f"MOTOR{robot_id:02d}",
        "startAngle": start_angle,
        "distance": distance,
        "endAngle": end_angle
    }
    
    topic = f"{TOPIC_PREFIX}/{robot_id}/command"
    message = json.dumps(command)
    
    print(f"Sending to {topic}: {message}")
    result = client.publish(topic, message)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Command sent successfully")
    else:
        print(f"Failed to send command: {result.rc}")
    
    return result

def main():
    # Create MQTT client
    client = mqtt.Client(
        client_id="Test_JSON_MQTT",
        protocol=mqtt.MQTTv5,
        transport='websockets'
    )
    
    # Set up callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    
    try:
        # Connect to broker
        print(f"Connecting to {BROKER}:{PORT}...")
        client.ws_set_options(path="/mqtt")
        client.connect(BROKER, PORT, 60)
        
        # Start the loop
        client.loop_start()
        
        # Subscribe to ESP32 data topics
        client.subscribe(f"{TOPIC_PREFIX}/+/data")
        print(f"Subscribed to {TOPIC_PREFIX}/+/data")
        
        # Wait for connection
        time.sleep(2)
        
        # Send test motor commands
        print("\n=== Sending Test Motor Commands ===")
        
        # Command 1: Move robot 1 forward
        send_motor_command(client, "01", 0, 50, 0)
        time.sleep(1)
        
        # Command 2: Turn robot 2
        send_motor_command(client, "02", 0, 30, 90)
        time.sleep(1)
        
        # Command 3: Complex movement for robot 3
        send_motor_command(client, "03", 45, 75, 135)
        time.sleep(1)
        
        # Command 4: Stop all robots
        send_motor_command(client, "ALL", 0, 0, 0)
        
        print("\n=== Test Commands Sent ===")
        print("Listening for responses... (Press Ctrl+C to exit)")
        
        # Keep listening for responses
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker")

if __name__ == "__main__":
    main() 