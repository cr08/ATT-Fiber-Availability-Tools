import sys
import time

import http.server
import socketserver

PORT = 3600

handler = http.server.SimpleHTTPRequestHandler

def start_server():
    httpd = socketserver.TCPServer(("", PORT), handler)
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()

start_server()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)