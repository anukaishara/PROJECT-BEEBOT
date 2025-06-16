import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker successfully!")
    else:
        print(f"Failed to connect to MQTT broker, return code: {rc}")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

def test_mqtt_connection():
    # Create MQTT client
    client = mqtt.Client(
        client_id="test_client",
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

    # Connect to broker (non-TLS WebSocket)
    broker_address = "broker.mqttdashboard.com"
    port = 8000
    
    print(f"Connecting to MQTT broker at {broker_address}:{port}...")
    
    try:
        client.connect(broker_address, port, 60)
        client.loop_start()
        
        # Subscribe to a test topic
        test_topic = "test/connection"
        client.subscribe(test_topic)
        print(f"Subscribed to topic: {test_topic}")
        
        # Publish a test message
        test_message = "Hello from test client!"
        client.publish(test_topic, test_message)
        print(f"Published message: {test_message}")
        
        # Wait for a few seconds to receive any messages
        time.sleep(5)
        
        # Clean up
        client.loop_stop()
        client.disconnect()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_mqtt_connection() 