import time
import socket
import threading

# Function to read data from the network
def readSerialData(sock, sharedData):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print(data)
                
                # data decoding
                if (data == b'OK\r\n'):
                    sharedData[0] = True
                    print("Sending Confirmed")
                elif (data == b'ERROR\r\n'):
                    sharedData[1] = True
        except socket.error as e:
            print(f"Socket error: {e}")
            break
        time.sleep(0.01)

def sendToSerial(sock, data):
    # sending data through the network
    data = data + "\n"
    try:
        sock.send(data.encode())
    except socket.error as e:
        print(f"Failed to send data: {e}")
        raise  # Re-raise the exception to handle it in the calling function

def serialAutoSend(sharedData, manual_mode=False, manual_event=None):
    print("serialAutoSend - Manual Mode" if manual_mode else "serialAutoSend - Automatic Mode")
    interval = 10  # 250ms between sends in auto mode
    reconnect_delay = 5  # seconds between reconnect attempts
    hosts = {
        '1': '192.168.192.79',  # ESP32 with ID=1
       # '2': '192.168.1.102'   # ESP32 with ID=2
    }
    port = 8080
    
    # Create a socket for each device
    sockets = {id: None for id in hosts}
    
    while True:
        try:
            # Connect to all devices
            for id, host in hosts.items():
                if sockets[id] is None:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        sock.connect((host, port))
                        sockets[id] = sock
                        print(f"Connected to device {id} at {host}")
                    except Exception as e:
                        print(f"Failed to connect to device {id}: {e}")
                        sockets[id] = None
            
            # Send data to all connected devices
            for id, sock in sockets.items():
                if sock is not None and sharedData[2]:  # If GUI enabled
                    print(f"Sending data to device {id}")
                    for id in sharedData[0]:  # If we have data for this ID
                        data = str(id) + ',' + ','.join(map(str, sharedData[0][id])) 
                        print("Network send:", data)
                        
                        try:
                            sock.sendall((data + "\n").encode())
                            # Wait for acknowledgment
                            ack = sock.recv(32)
                            if not ack:
                                raise ConnectionError("Connection closed")
                            print(f"Device {id} response: {ack.decode().strip()}")
                        except Exception as e:
                            print(f"Error with device {id}: {e}")
                            sockets[id] = None  # Mark for reconnection
            
            if manual_mode:
                # Wait for manual trigger event
                if manual_event and manual_event.wait(1.0):  # Check every second if we should send
                    manual_event.clear()
                    continue
            else:
                # Automatic mode - sleep for interval
                time.sleep(interval)
            
        except Exception as e:
            print(f"System error: {e}")
            # Close all sockets on error
            for id in sockets:
                if sockets[id] is not None:
                    sockets[id].close()
                    sockets[id] = None
            print(f"Reconnecting in {reconnect_delay} seconds...")
            time.sleep(reconnect_delay)

# Example usage:
if __name__ == "__main__":
    # Shared data structure example
    shared_data = [
        {'1': [ -90, 0, 0]},  # Data for devices
        False,  # Error flag
        True    # GUI enabled flag
    ]
    
    # For manual mode:
    manual_event = threading.Event()
    
    # Start in manual mode
    serial_thread = threading.Thread(
        target=serialAutoSend,
        args=(shared_data, True, manual_event),
        daemon=True
    )
    serial_thread.start()
    
    # To manually trigger a send:
    while True:
        input("Press Enter to send data manually...")
        manual_event.set()  # This will trigger the send in the serial thread
        
        # You could also update the shared_data here if needed
        # shared_data[0]['1'] = [5, 6, 7, 8]  # Update data for device 1