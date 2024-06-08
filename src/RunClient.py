from socket import socket

server_addr = "127.0.0.1"
port = 7777
client = socket()
client.connect((server_addr, port))

print(client.recv(1024).decode())
client.send("Success!".encode())

client.close()
del client
