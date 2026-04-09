import socket
import sys


server = socket.socket()

server.bind(("localhost", 8080))

server.listen()
print("Server is listening...")

client, address = server.accept()
print("Client connected", address)

#set up get request
data = client.recv(1024)
print(data)
print(data.decode())