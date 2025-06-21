import time
import socket

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

def serialAutoSend(sharedData):
    interval = 0.25  # frequency in seconds
    host = '192.168.192.79'  # replace with your server IP
    port = 8080     # replace with your server port
    
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        while True:
            if sharedData[2]:  # if operator GUI enabled
                for key in sharedData[0]:
                    data = str(key) + ',' + ','.join(map(str, sharedData[0][key])) + ','
                    #print("Network send:", data)
                    sendToSerial(sock, data)
                    time.sleep(interval)
    except socket.error as e:
        print(f"Network error: {e}")
    finally:
        sock.close()