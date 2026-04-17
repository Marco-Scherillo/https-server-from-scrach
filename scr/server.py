import socket
import sys

#Start server
server = socket.socket()
server.bind(("localhost", 8080))
server.listen()
print("Server is listening...")

#unpack client data 
client, address = server.accept()
print("Client connected", address)

#set up get request
data = client.recv(1024)
request = data.decode()

lines, body = request.split("\r\n\r\n")

lines = lines.split("\r\n")
method, path, version = lines[0].split(" ")

headers = {}
for line in lines[1:]:
    if line == " ":
        break
    key, value = line.split(":", 1)
    headers[key] = value

#routing 
if path == "/":
    responce_body = f"{method} Home Page"
elif path == "/Hello":
    responce_body = f"{method} Hello Marco"
elif path == "/close":
    responce_body = f"{method} Connection Closed BYEEEE"
else:
    responce_body = f"{method} 404 not found"


response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: Text/plain\r\n"
    f"content-Lenght: {len(responce_body)}\r\n"
    "\r\n"
    f"{responce_body}"
)

#Close connection
client.sendall(response.encode())
client.close()

