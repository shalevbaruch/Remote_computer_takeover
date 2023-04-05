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
        if first_screenshot:
            first_screenshot = False
            keysSock = connect_My_Server(client_ip, client_listening_port)
            t1  = threading.Thread(target=sendKeys)
            mouseSock = connect_My_Server(client_ip, client_listening_port)
            t2 = threading.Thread(target=sendMouse)
            t1.start()
            t2.start()
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
        print("done receiving image :{}".format(len(bytes_recieved)))


#הערה למחר - עבור הפונקציה של המפתחות והעכבר נרצה לשלוח כמה דברים - באיזה סוג הודעה מדובר כלומר של מקלדת או של עכבר, ואז לדוגמא עבור המקלדת נגיד באיזה סוג לחיצה זה כלומר לחיצה או
#עזיבה של אותו לחצן,  


def sendKeys():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def sendMouse(mouseSock):
    pass



def on_press(key):
    key_repr = key.char if hasattr(key, 'char') else key.name
    keysSock.sendall("1")
    keysSock.sendall(len(key_repr).to_bytes(4, byteorder='big'))
    keysSock.sendall(key_repr)


def on_release(key):
    key_repr = key.char if hasattr(key, 'char') else key.name
    keysSock.sendall("2")
    keysSock.sendall(len(key_repr).to_bytes(4, byteorder='big'))
    keysSock.sendall(key_repr)




def connect_My_Server(Server_IP, Server_Port):
    server_address = (Server_IP, Server_Port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock)  # add a security layer
    ssl_sock.connect(server_address)    
    return ssl_sock


if __name__ == '__main__':
    screenshotServer = My_Server(listen_port=9124, simultaneous_requests_limit=1, handle=handleScreenshot, is_secured=True)
    screenshotServer.start()



