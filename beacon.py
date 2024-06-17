import socket
import ssl

def create_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # secure_socket = context.wrap_socket(client_socket, server_hostname=server_ip)
    client_socket.connect((server_ip, server_port))
    while True:
        client_socket.send("Hello Server".encode())
        response = client_socket.recv(10240)
        print(f"Received: {response.decode()}")
        client_socket.send(input("-->").encode())
        if(response=="nuke"):
            break
    client_socket.close()


    

if __name__ == "__main__":
    create_client("127.0.0.1", 9999)
