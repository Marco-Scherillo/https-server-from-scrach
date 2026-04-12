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

request = data.decode()

lines = request.split("\r\n")
for line in lines:
    print(line)

request = lines[0].split()

method = request[0]
path = request[1]
version = request[2]

headers = {}

for i in range(1, len(lines)):
    line = lines[i].split(":")
    if len(line) > 1:
        headers[line[0]] = line[1]

print(headers)

body = "Hello World"

response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: Text/plain\r\n"
    f"content-Lenght: {len(body)}\r\n"
    "\r\n"
    f"{body}"
)

client.sendall(response.encode())
