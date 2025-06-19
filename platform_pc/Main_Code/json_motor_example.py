#!/usr/bin/env python3
"""
Simple example showing how to send JSON motor commands via MQTT
This demonstrates the new JSON-based communication system
"""

import paho.mqtt.client as mqtt
import json
import time

class JSONMotorController:
    def __init__(self, broker="broker.mqttdashboard.com", port=8000):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(
            client_id="JSON_Motor_Controller",
            protocol=mqtt.MQTTv5,
            transport='websockets'
        )
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.is_connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.is_connected = True
        
    def on_publish(self, client, userdata, mid):
        print(f"Message {mid} published successfully")
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.ws_set_options(path="/mqtt")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            time.sleep(1)  # Wait for connection
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        self.is_connected = False
        
    def send_motor_command(self, robot_id, start_angle, distance, end_angle):
        """Send a motor command in JSON format"""
        if not self.is_connected:
            print("Not connected to MQTT broker")
            return False
            
        command = {
            "id": f"MOTOR{robot_id:02d}",
            "startAngle": start_angle,
            "distance": distance,
            "endAngle": end_angle
        }
        
        topic = f"swarm/esp32/{robot_id}/command"
        message = json.dumps(command)
        
        print(f"Sending: {message}")
        print(f"To topic: {topic}")
        
        result = self.client.publish(topic, message)
        return result.rc == mqtt.MQTT_ERR_SUCCESS
        
    def move_forward(self, robot_id, distance=50):
        """Move robot forward"""
        return self.send_motor_command(robot_id, 0, distance, 0)
        
    def turn_left(self, robot_id, angle=90):
        """Turn robot left"""
        return self.send_motor_command(robot_id, 0, 30, angle)
        
    def turn_right(self, robot_id, angle=90):
        """Turn robot right"""
        return self.send_motor_command(robot_id, 0, 30, -angle)
        
    def stop_robot(self, robot_id):
        """Stop robot movement"""
        return self.send_motor_command(robot_id, 0, 0, 0)
        
    def stop_all_robots(self):
        """Stop all robots"""
        return self.send_motor_command("ALL", 0, 0, 0)

def main():
    """Example usage of JSON motor controller"""
    controller = JSONMotorController()
    
    if not controller.connect():
        print("Failed to connect to MQTT broker")
        return
        
    print("Connected to MQTT broker")
    print("Sending test motor commands...")
    
    try:
        # Example 1: Move robot 01 forward
        print("\n1. Moving robot 01 forward...")
        controller.move_forward("01", 50)
        time.sleep(2)
        
        # Example 2: Turn robot 02 left
        print("\n2. Turning robot 02 left...")
        controller.turn_left("02", 90)
        time.sleep(2)
        
        # Example 3: Turn robot 03 right
        print("\n3. Turning robot 03 right...")
        controller.turn_right("03", 90)
        time.sleep(2)
        
        # Example 4: Complex movement for robot 04
        print("\n4. Complex movement for robot 04...")
        controller.send_motor_command("04", 45, 75, 135)
        time.sleep(2)
        
        # Example 5: Stop all robots
        print("\n5. Stopping all robots...")
        controller.stop_all_robots()
        
        print("\nAll test commands sent!")
        
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        controller.disconnect()
        print("Disconnected from MQTT broker")

if __name__ == "__main__":
    main() 