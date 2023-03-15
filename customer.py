import time
import os
from PIL import ImageGrab
import sys
import socket
import ssl
import select
from io import BytesIO



def sendScreenshot(ssl_sock):
    img = ImageGrab.grab()
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    img_data = buffer.getvalue()
    ssl_sock.sendall(img_data)




    # screenshot_bytes = screenshot.to_bytes(4, )
    # print(screenshot_bytes)
    # size = len(screenshot_bytes)
    # ssl_sock.sendall(size.to_bytes(4, byteorder='big'))
    # ssl_sock.sendall(screenshot_bytes)
    # for data in screenshot_bytes:
    #     ssl_sock.sendall(data.to_bytes())

    





if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connecting to remote computer 9124
    ssl_sock = ssl.wrap_socket(sock)  # add a security layer
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 9124
    server_address = (SERVER_IP, SERVER_PORT)
    ssl_sock.connect(server_address)
    print(ssl_sock.recv(8).decode())  # welcome message
    sendScreenshot(ssl_sock)
    # while True:
    #     sendScreenshot(ssl_sock)
    #     readable, _, _ = select.select([ssl_sock], [], [])
    #     if readable:
    #         message = ssl_sock.recv(1024).decode()
    #         print(message)
    #     time.sleep(1/60)

