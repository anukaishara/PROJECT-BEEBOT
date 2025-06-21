import socket
import time

def debug_socket_data():
    host = '192.168.192.79'
    port = 8080
    
    # Simulate the data structure that would be in sharedData[0]
    # This is what broadcastPos would contain
    simulated_broadcast_pos = {
        19: (0.1234, 45.6789, 0.0),  # Example: (start_turn, distance, end_angle)
        20: (0.2345, 67.8901, 0.0),
        21: (0.3456, 89.0123, 0.0)
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        print(f"Connecting to {host}:{port}")
        
        sock.connect((host, port))
        print(f"Connected successfully")
        
        # Simulate the data sending loop from socketCom.py
        interval = 0.25
        for i in range(5):  # Send 5 messages
            print(f"\n--- Sending data #{i+1} ---")
            
            for key in simulated_broadcast_pos:
                # This is the exact format from socketCom.py line 44
                data = str(key) + ',' + ','.join(map(str, simulated_broadcast_pos[key])) + ','
                print(f"Preparing to send: {data}")
                
                # Add newline as in sendToSerial function
                data_with_newline = data + "\n"
                print(f"Actual data sent: {data_with_newline.strip()}")
                
                try:
                    sock.send(data_with_newline.encode())
                    print("Data sent successfully")
                except socket.error as e:
                    print(f"Failed to send data: {e}")
                    break
                
                time.sleep(interval)
                
            # Try to receive any response
            try:
                response = sock.recv(1024)
                if response:
                    print(f"Received: {response}")
            except socket.timeout:
                print("No response (timeout)")
            except socket.error as e:
                print(f"Error receiving: {e}")
                
    except socket.error as e:
        print(f"Connection error: {e}")
    finally:
        sock.close()
        print("Connection closed")

if __name__ == "__main__":
    debug_socket_data() 