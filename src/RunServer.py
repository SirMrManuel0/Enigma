# some simple testing
import logging
from socket import socket

# Setting up the logger
logger = logging.getLogger("Server Logger")
logger.setLevel(logging.INFO)  # Set the logging level

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # Set the logging level for the handler

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

# Socket setup
server = socket()
port = 7777
server.bind(("127.0.0.1", port))
logger.info("Server is ready.")
logger.info("Server awaits on port %d", port)
server.listen()

client, address = server.accept()
logger.info("Client accepted with Address: %s", address)
client.send("Test call".encode())
print("received", client.recv(1024).decode())
client.close()
server.close()
del server
del client
