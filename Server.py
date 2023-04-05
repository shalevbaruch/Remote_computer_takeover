import sys
sys.path.append("C:/University")  # This is the path on my desktop computer
sys.path.append("C:/University/Cyber/networks")  #This is the path on my laptop
import os
import threading
import keyboard
import time
import socket
import ssl
from pynput.keyboard import Key, Listener
import ctypes

try:
    from Sending_Files_System.general_server import My_Server
except ImportError:
    from ..Sending_Files_System.general_server import My_Server


first_screenshot = True # when we get the first screenshot, it means the client already set up the server for mouse and keyboard
client_listening_port = 9200
client_ip = "10.0.0.60"
keysSock = None
mouseSock = None

def handleScreenshot(ssl_client_soc, ssl_client_soc_address):
    while True:
        global first_screenshot
        global keysSock
        global mouseSock
        if first_screenshot:
            first_screenshot = False
            keysSock = connect_My_Server(client_ip, client_listening_port)
            sendKeys()
        #     t1  = threading.Thread(target=sendKeys)
        #     mouseSock = connect_My_Server(client_ip, client_listening_port)
        #     t2 = threading.Thread(target=sendMouse)
        #     t1.start()
        #     t2.start()
        screenshot_size = ssl_client_soc.recv(4)
        screenshot_size = int.from_bytes(screenshot_size, byteorder='big')
        print("Received image size :{}".format(screenshot_size))
        screenshot = b''
        bytes_recieved = 0 
        to_recieve = 1024
        while bytes_recieved < screenshot_size:
            screenshot_part =  ssl_client_soc.recv(to_recieve)
            screenshot += screenshot_part
            bytes_recieved += len(screenshot_part)
            if screenshot_size - bytes_recieved < 1024:
                to_recieve = screenshot_size - bytes_recieved
        
        


#הערה למחר - עבור הפונקציה של המפתחות והעכבר נרצה לשלוח כמה דברים - באיזה סוג הודעה מדובר כלומר של מקלדת או של עכבר, ואז לדוגמא עבור המקלדת נגיד באיזה סוג לחיצה זה כלומר לחיצה או
#עזיבה של אותו לחצן,  asdfhfd!==


# def on_press(key):
#     key_repr = key.char if hasattr(key, 'char') else key.name
#     print(key_repr)
#     print(type(key_repr))
#     if key_repr is not None:
#         keysSock.sendall("1".encode())
#         keysSock.sendall(len(key_repr).to_bytes(4, byteorder='big'))
#         keysSock.sendall(key_repr.encode())


# def on_release(key):
#     key_repr = key.char if hasattr(key, 'char') else key.name
#     if key_repr is not None:
#         keysSock.sendall("2".encode())
#         keysSock.sendall(len(key_repr).to_bytes(4, byteorder='big'))
#         keysSock.sendall(key_repr.encode())

def is_capslock_on():
    return True if ctypes.WinDLL("User32.dll").GetKeyState(0x14) else False



def sendKeys():
    keysSock.sendall("4".encode())
    capslock_on = is_capslock_on()
    if capslock_on:
        keysSock.sendall("1".encode())
    else:
        keysSock.sendall("0".encode())
    while True:
        event = keyboard.read_event()
        event_type = event.event_type
        event_name = event.name
        if event_type == "down":
            keysSock.sendall("1".encode())
        elif event_type == "up":
            keysSock.sendall("2".encode())
        keysSock.sendall(len(event_name).to_bytes(4, byteorder='big'))
        keysSock.sendall(event_name.encode())


def sendMouse(mouseSock):
    pass








def connect_My_Server(Server_IP, Server_Port):
    server_address = (Server_IP, Server_Port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock)  # add a security layer
    ssl_sock.connect(server_address)    
    return ssl_sock


if __name__ == '__main__':
    screenshotServer = My_Server(listen_port=9124, simultaneous_requests_limit=1, handle=handleScreenshot, is_secured=True)
    screenshotServer.start()



