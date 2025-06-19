import paho.mqtt.client as mqtt
import time
import json

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker successfully!")
    else:
        print(f"Failed to connect to MQTT broker, return code: {rc}")

def on_message(client, userdata, msg):
    try:
        # Try to parse as JSON
        data = json.loads(msg.payload.decode())
        print(f"Received JSON message on topic {msg.topic}: {data}")
    except json.JSONDecodeError:
        # If not JSON, print as plain text
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

def send_json_motor_command(client, robot_id, start_angle, distance, end_angle):
    """Send a motor command in JSON format"""
    command = {
        "id": f"MOTOR{robot_id:02d}",
        "startAngle": start_angle,
        "distance": distance,
        "endAngle": end_angle
    }
    
    topic = f"swarm/esp32/{robot_id}/command"
    message = json.dumps(command)
    
    print(f"Sending JSON command to {topic}: {message}")
    result = client.publish(topic, message)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("JSON command sent successfully")
    else:
        print(f"Failed to send JSON command: {result.rc}")
    
    return result

def test_mqtt_connection():
    # Create MQTT client
    client = mqtt.Client(
        client_id="mqttx_ccb44c85",
        protocol=mqtt.MQTTv5,
        transport='websockets'
    )

    # Set up callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Configure WebSocket connection
    client.ws_set_options(
        path="/mqtt",
        headers=None
    )

    # Connect to broker (WebSocket)
    broker_address = "broker.mqttdashboard.com"
    port = 8000  # WebSocket port
    
    print(f"Connecting to MQTT broker at {broker_address}:{port}...")
    
    try:
        client.connect(broker_address, port, 60)
        client.loop_start()
        
        # Subscribe to ESP32 topics
        client.subscribe("swarm/esp32/+/data")
        client.subscribe("swarm/esp32/+/command")
        print("Subscribed to ESP32 topics")
        
        # Wait for connection to establish
        time.sleep(2)
        
        # Send test JSON motor commands
        print("\n=== Sending Test JSON Motor Commands ===")
        
        # Test command 1: Move robot 01 forward
        send_json_motor_command(client, "01", 0, 50, 0)
        time.sleep(1)
        
        # Test command 2: Turn robot 02
        send_json_motor_command(client, "02", 0, 30, 90)
        time.sleep(1)
        
        # Test command 3: Complex movement for robot 03
        send_json_motor_command(client, "03", 45, 75, 135)
        time.sleep(1)
        
        # Test command 4: Stop all robots
        send_json_motor_command(client, "ALL", 0, 0, 0)
        
        print("\n=== Test JSON Commands Sent ===")
        print("Listening for responses... (Press Ctrl+C to exit)")
        
        # Wait for a few seconds to receive any messages
        time.sleep(10)
        
        # Clean up
        client.loop_stop()
        client.disconnect()
        print("Test completed successfully!")
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_mqtt_connection() 