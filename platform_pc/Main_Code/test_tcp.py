import socket

def start_server(host='0.0.0.0', port=65432):  # Changed to 0.0.0.0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            s.listen()
            print(f"Server listening on {host}:{port}")
            
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data.decode()}")
                    
                    # Optional: Send a response
                    response = input("Enter response to send back (or press enter to continue): ")
                    if response:
                        conn.sendall(response.encode())
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_server()