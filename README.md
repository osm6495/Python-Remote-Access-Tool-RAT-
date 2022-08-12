# Python-Remote-Access-Tool-RAT-
Python Remote Access Tool (RAT) with communication between server and client encrypted with TLS.

Included privkey.pem and certificate.pem are default TLS certs for testing purposes only. Replace them if you want to actually encrypt traffic, to use replacement private key and cert, replace the keyfile and certfile path in the make_connection() function in both client.py and server.py
