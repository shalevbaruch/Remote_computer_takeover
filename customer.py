import time
import os
from PIL import ImageGrab

import sys
sys.path.append("C:/University")  # This is the path on my desktop computer
sys.path.append("C:/University/YoungForTech/networks")  #Thie is the path on my laptop

import socket
import ssl
import select
from io import BytesIO
import threading
import keyboard



try:
    from Sending_Files_System.server import My_Server
except ImportError:
    from ..Sending_Files_System.server import My_Server





def sendScreenshot(sock):  # we use this function only while using UDP protocol
    img = ImageGrab.grab()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_data = buffer.getvalue()
    size = len(img_data)
    sock.sendall(size.to_bytes(4, byteorder='big'))
    sock.sendall(img_data)
    # sock.sendto(size.to_bytes(4, byteorder='big'), server_address)
    # imgParts = split_bytes(img_data)
    # for imgPart in imgParts:
    #     sock.sendto(imgPart, server_address)


def screenshotLoop(sock):
    while True:
        sendScreenshot(sock)
        time.sleep(1/60)


def split_bytes(byte_data):
    byte_list = []
    length = len(byte_data)
    i = 0
    while i < length:
        # Split the data into chunks of 1 KB each
        chunk_size = min(1024, length - i)
        chunk = byte_data[i:i+chunk_size]
        byte_list.append(chunk)
        i += chunk_size
    return byte_list


def connect_My_Server(Server_IP, Server_Port, Transport_Layer_Protocol):
    server_address = (Server_IP, Server_Port)
    if Transport_Layer_Protocol == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    else:  # Transport_Layer_Protocol == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(sock)  # add a security layer
        ssl_sock.connect(server_address)     
    return ssl_sock


def getKeys(server,keysSock):
    while True:
        data = keysSock.recv(1024)
        if not data:
            break
        key = data.decode()
        keyboard.press(key)
        keyboard.release(key)


def handleKeysAndMouse(keysAndMouseSock, recieverSock):
    pass





if __name__ == "__main__":
    keysPort = 9200
    keysSock = My_Server(LISTEN_PORT=keysPort, SIMULTANEOUS_REQUESTS_LIMIT=1,TRANSPORT_LAYER_PROTOCOL="TCP",HANDLE=getKeys)
    t2 = threading.Thread(target=keysSock.start)
    t2.start()


    # screenshot_server_ip = "127.0.0.1" 
    screenshot_server_ip = "10.0.0.35"   # when I'm using my Desktop computer as Server.py and I'm at home
    screenshot_server_Port = 9124
    Transport_Layer_Protocol = "TCP"
    screenshotSock = connect_My_Server(screenshot_server_ip, screenshot_server_Port, Transport_Layer_Protocol)
    t1 = threading.Thread(target=screenshotLoop, args=(screenshotSock,))  # thread for sending screenshots
    t1.start()
    


    t2.join()
    t1.join()


    



    # keys_server_port = 9200
    # keys_Transport_Layer_Protocol = "TCP"
    # keysClientSock, keys_server_address = connect_My_Server(Server_IP, keys_server_port, keys_Transport_Layer_Protocol)
    # t2 = threading.Thread(target=getKeys, args=(keysClientSock,))
    # t2.start()

    #t1.join()
    # t2.join()
    # t1.join()
