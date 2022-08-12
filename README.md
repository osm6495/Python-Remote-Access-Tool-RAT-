
# Python Remote Access Tool (RAT)

Python Remote Access Tool (RAT) with communication between server and client encrypted with TLS. It should work on Linux, Windows, and Mac machines, but I haven't been able to test it on a Mac to be sure.

Included privkey.pem and certificate.pem are default TLS certs for testing purposes only. Replace them if you want to actually encrypt traffic, to use replacement private key and cert, replace the keyfile and certfile path in the make_connection() function in both client.py and server.py

# Requirements
This program only uses the standard python library, so the only thing you need to install in order to run it is Python 3 which can be downloaded here: https://www.python.org/downloads/

# Usage
Run server.py and then client.py, the client should be run on the target machine, but the server can be run on any machine. Once you have started both, the server should look like this.
```
$python3 server.py
Connected to client
Python Rat>
```
By putting commands into this input, they are sent to the client and run on the client machine. Keep in mind that currently, commands are run by subprocess, which means you will not have permission or ability to run things like mkdir and cd. 
```
Python Rat>ls
LICENSE
README.md
certficate.pem
client.py
privkey.pem
rat.db
server.py
Python Rat>pwd
/mnt/c/Users/Owen/Documents/Code/Python-RAT
Python Rat>killrat
Closing Rat
```
The killrat command closes the program, and the rathistory command shows the command history database.
```
Python Rat>ls
LICENSE
README.md
certficate.pem
client.py
privkey.pem
rat.db
server.py
Python Rat>rathistory
('2022-08-12 16:45:14.328810', 'ls', 'LICENSE\nREADME.md\ncertficate.pem\nclient.py\nprivkey.pem\nrat.db\nserver.py')
Python Rat>
```
The first item in each row is the datetime that the results of the command were recieved from the server. This is also used as a primary key to identify each entry in the database The second item is the command that was sent. The third item is the output results.

# Server Configuration
If you want to change the IP or Port of the client or server, just edit the initialization of the server or client object at the bottom of the python files.

## client.py
```
if __name__ ==  "__main__":
client = CLIENT("127.0.0.1", 4444) #Client IP and Port
client.make_connection("127.0.0.1", 4445) #Should match server IP and Port (Configure in server.py)
client.execute() #Run the rat
```

## server.py
```
if __name__ ==  "__main__":
server = SERVER("127.0.0.1", 4445) #Server IP and Port
server.make_connection()
server.make_db()
server.execute()
```
