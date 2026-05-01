import socket
import sys
import threading
import ssl

def parse_request(data):
    request = data.decode()
    status_code = 400

    lines, body = request.split("\r\n\r\n")

    lines = lines.split("\r\n")
    method, path, version = lines[0].split(" ")

    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(":", 1)
        headers[key] = value

    #routing 
    if path == "/":
        response_body = f"{method} Home Page"
        status_code = 200
    elif path == "/Hello":
        response_body = f"{method} Hello Marco"
        status_code = 200
    else:
        response_body = f"{method} 404 not found"
        status_code = 404
    
    return status_code, response_body

def handle_response(status_code, response_body):
    status_text = {
        200 : "OK",
        404 : "Not Found"
    }
    return (
        f"HTTP/1.1 {status_code} {status_text[status_code]}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n"
        f"{response_body}"
        )
    





def handle_client(client):
    #set up get request
    data = client.recv(1024)
    
    status_code, response_body = parse_request(data)
    response = handle_response(status_code, response_body)
    #Close connection
    client.sendall(response.encode())
    client.close()

def start_server():
    while True:
        #unpack client data 
        client, address = server.accept()
        print("Client connected", address)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


#Start server
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # tell OS that the port can be reused right away after its closed.
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="../certs/cert.pem", keyfile="../certs/key.pem")
server = context.wrap_socket(server, server_side=True)
server.bind(("localhost", 8080))
server.listen()
print("Server is listening...")

server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

input("Press Enter to stop server...\n")
print("Shutting Down")
server.close()
