# JSON Migration Guide

## Overview
This document explains the migration from Protocol Buffers to JSON format for MQTT communication in the robot control system.

## Changes Made

### 1. Main Program (`mainProg.py`)
- **Removed**: `from MQTT_msg_pb2 import *` import
- **Added**: JSON-based motor command generation
- **Updated**: `destinationCalculation()` function to send JSON commands instead of protobuf

#### Before (Protocol Buffers):
```python
# Create protobuf message
newBotPosArr = BotPositionArr()
newBot = BotPosition()
newBot.bot_id = i
newBot.x_cod = robots_data[i].init_pos[0]/(ROI['end_x']-ROI['start_x'])*30 
newBot.y_cod = robots_data[i].init_pos[1]/(ROI['end_x']-ROI['start_x'])*30
newBot.angle = 0
newBotPosArr.positions.append(newBot)

# Send protobuf data
data = newBotPosArr.SerializeToString()
client.publish(TOPIC_SEVER_BOT_POS, data)
```

#### After (JSON):
```python
# Create JSON command
robot_command = {
    "id": f"Robo{keys[i]}",
    "startAngle": int(Dir),
    "distance": int(F/1000),
    "endAngle": int(Dir + 10)
}
robot_commands.append(robot_command)

# Send JSON data
for robot_command in robot_commands:
    topic = f"swarm/esp32/{robot_command['id']}/command"
    client.publish(topic, json.dumps(robot_command))
```

### 2. WiFi Communication (`wifiCom.py`)
- Already using JSON format
- No changes needed
- Sends motor commands in JSON format: `{"id":"MOTOR01","startAngle":0,"distance":50,"endAngle":60}`

### 3. Test Files
- **Updated**: `test_mqtt.py` to send JSON motor commands
- **Created**: `test_json_mqtt.py` for comprehensive JSON testing
- **Created**: `json_motor_example.py` for simple JSON motor control examples

## JSON Message Format

### Motor Commands
```json
{
    "id": "MOTOR01",
    "startAngle": 0,
    "distance": 50,
    "endAngle": 60
}
```

### Field Descriptions
- `id`: Robot identifier (e.g., "MOTOR01", "MOTOR02")
- `startAngle`: Starting angle in degrees (0-360)
- `distance`: Distance to travel in arbitrary units
- `endAngle`: Ending angle in degrees (0-360)

### Topics
- **Commands**: `swarm/esp32/{robot_id}/command`
- **Data**: `swarm/esp32/{robot_id}/data`

## Usage Examples

### 1. Simple Motor Control
```python
from json_motor_example import JSONMotorController

controller = JSONMotorController()
controller.connect()

# Move robot forward
controller.move_forward("01", 50)

# Turn robot left
controller.turn_left("02", 90)

# Stop all robots
controller.stop_all_robots()
```

### 2. Custom Motor Commands
```python
# Send custom JSON command
command = {
    "id": "MOTOR01",
    "startAngle": 45,
    "distance": 75,
    "endAngle": 135
}

topic = "swarm/esp32/01/command"
client.publish(topic, json.dumps(command))
```

### 3. Testing JSON Communication
```bash
# Run the test script
python test_json_mqtt.py

# Run the example script
python json_motor_example.py
```

## Benefits of JSON Migration

1. **Human Readable**: JSON messages are easy to read and debug
2. **No Dependencies**: No need for protobuf compiler or generated files
3. **Flexible**: Easy to modify message structure without recompiling
4. **Web Compatible**: JSON works natively with web applications
5. **Debugging**: Easier to log and inspect message contents

## Migration Checklist

- [x] Remove protobuf imports from `mainProg.py`
- [x] Update motor command generation to use JSON
- [x] Update MQTT publishing to send JSON messages
- [x] Verify `wifiCom.py` already uses JSON
- [x] Update test files to use JSON format
- [x] Create example scripts for JSON usage
- [x] Test JSON communication with MQTT broker

## Testing

1. **Run JSON Test**: `python test_json_mqtt.py`
2. **Run Example**: `python json_motor_example.py`
3. **Run Main Program**: `python mainProg.py`
4. **Monitor MQTT**: Use MQTT client to verify JSON messages

## Troubleshooting

### Common Issues
1. **JSON Decode Error**: Ensure messages are valid JSON
2. **Topic Mismatch**: Verify topic format matches ESP32 expectations
3. **Connection Issues**: Check MQTT broker connection settings

### Debug Commands
```python
# Print JSON message before sending
print(f"Sending: {json.dumps(command, indent=2)}")

# Verify JSON format
import json
try:
    parsed = json.loads(message)
    print("Valid JSON")
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

## Next Steps

1. Test with actual ESP32 devices
2. Verify motor responses to JSON commands
3. Update any ESP32 code to handle JSON format
4. Monitor system performance with JSON vs protobuf
5. Consider adding message validation and error handling 