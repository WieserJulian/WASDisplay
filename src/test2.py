import socket

SERVER_HOST = "localhost"
SERVER_PORT = 8080
BUFFER_SIZE = 4096
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(10)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# accept connection if there is any
client_socket, address = s.accept()
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")
while True:
    received = client_socket.recv(BUFFER_SIZE).decode()
    print(received)