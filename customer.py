import time
from PIL import ImageGrab
# AAASaasbbBVCNCXZBNM,KJHGFDSERTYUIOLP98)()bvcnmjut12543זסבהנמצתתלחיעכSAFGHTERF
import sys
sys.path.append("C:/University")  # This is the path on my desktop computer
sys.path.append("C:/University/Cyber/networks")  #Thie is the path on my laptop
import socket
import ssl
from io import BytesIO
import threading
import keyboard
import win32api
import win32con

try:
    from Sending_Files_System.general_server import My_Server
except ImportError:
    from ..Sending_Files_System.general_server import My_Server





def sendScreenshot(sock):  
    img = ImageGrab.grab()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_data = buffer.getvalue()
    size = len(img_data)
    sock.sendall(size.to_bytes(4, byteorder='big'))
    sock.sendall(img_data)


def screenshotLoop(sock):
    while True:
        sendScreenshot(sock)
        time.sleep(1/60)


def connect_My_Server(Server_IP, Server_Port):
    server_address = (Server_IP, Server_Port) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock)  # add a security layer
    ssl_sock.connect(server_address)     
    return ssl_sock


def press_key(keysSock):
    is_scancode = int(keysSock.recv(1).decode())
    key_length = keysSock.recv(4)
    key_length = int.from_bytes(key_length, byteorder='big')
    # print(key_length)
    if is_scancode:
        key_scancode = keysSock.recv(key_length)
        key_scancode = int.from_bytes(key_scancode, byteorder='big')
        # print(key_scancode)
        win32api.keybd_event(key_scancode, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
    else:
        key = keysSock.recv(key_length).decode()
        # print(key)
        keyboard.press(key)


def release_key(keysSock):
    is_scancode = int(keysSock.recv(1).decode())
    key_length = keysSock.recv(4)
    key_length = int.from_bytes(key_length, byteorder='big')
    if is_scancode:
        key_scancode = keysSock.recv(key_length)
        key_scancode = int.from_bytes(key_scancode, byteorder='big')
        win32api.keybd_event(key_scancode, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    else:
        key = keysSock.recv(key_length).decode()
        keyboard.release(key)


def handle_mouse():
    pass 

    
def handleKeysAndMouse(keysOrMouseSock, keysOrMouseSock_address):
    while True:
        message_type = keysOrMouseSock.recv(1).decode()
        if message_type == "1":
            press_key(keysOrMouseSock)
        elif message_type == "2":
            release_key(keysOrMouseSock)
        elif message_type == "3":
            handle_mouse()
        






if __name__ == "__main__":
    keysPort = 9200
    keysSock = My_Server(listen_port=keysPort, simultaneous_requests_limit=2, handle=handleKeysAndMouse, is_secured=True)
    t2 = threading.Thread(target=keysSock.start)
    t2.start()


    # screenshot_server_ip = "127.0.0.1" 
    screenshot_server_ip = "10.0.0.35"   # when I'm using my Desktop computer as Server.py and I'm at home
    screenshot_server_Port = 9124
    screenshotSock = connect_My_Server(screenshot_server_ip, screenshot_server_Port)
    screenshotLoop(screenshotSock)
    
