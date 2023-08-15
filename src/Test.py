# the ip address or hostname of the server, the receiver
import socket

from tqdm.contrib import logging

host = "localhost"
# the port, let's use 5001
port = 8080
# create the client socket
s = socket.socket()
logging.info(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
s.send("Hello World".encode())
