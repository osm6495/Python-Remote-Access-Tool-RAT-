"""
Python Remote Access Tool(RAT) Client

This client requests commands from a server and executes them on the machine. All traffic is encrypted with TLS.
"""

import os
import socket
import ssl
from time import sleep #Testing ONLY

class CLIENT:
    """
    Client object

    Requests tasks from the RAT server and executes them on the machine.
    
    Attributes:
        host : str
            IP address of the client
        port : int
            Port of the client
        cwd : str
            Current working directory on the machine
    
    Methods:
        make_connection()
            Connect to the server
        execute()
            TODO
    TODO
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
        self.cwd = os.getcwd()

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
        while True:
            sock.send("Hello World!".encode("utf-8"))
            sleep(1)

if __name__ == "__main__":
    client = CLIENT("127.0.0.1", 4444) #Initialize client
    client.make_connection("127.0.0.1", 4445) #Connect to server
    client.execute() #Run the rat