import time
import os
from PIL import ImageGrab
# AAASaasbbBVCNCXZBNM,KJHGFDSERTYUIOLP98)()bvcnmjut12543זסבהנמצתתלחיעכSAFGHTERF
import sys
sys.path.append("C:/University")  # This is the path on my desktop computer
sys.path.append("C:/University/Cyber/networks")  #Thie is the path on my laptop

import socket
import ssl
import select
from io import BytesIO
import threading
import keyboard
import ctypes
import win32api


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
    key_length = keysSock.recv(4)
    key_length = int.from_bytes(key_length, byteorder='big')
    key = keysSock.recv(key_length).decode()
    keyboard.press(key)


def release_key(keysSock):
    key_length = keysSock.recv(4)
    key_length = int.from_bytes(key_length, byteorder='big')
    key = keysSock.recv(key_length).decode()
    keyboard.release(key)


def handle_mouse():
    pass 


def is_capslock_on():
    return True if ctypes.WinDLL("User32.dll").GetKeyState(0x14) else False


def is_english():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2**16 - 1)
    lid_hex = hex(lid)
    return lid_hex == "0x409"


def capslock_adjustment(keysSock):
    capslock_on = is_capslock_on()
    server_capslock_on = int(keysSock.recv(1).decode())
    if (server_capslock_on and capslock_on) or (not server_capslock_on and not capslock_on):
        return
    else:
        keyboard.press("caps lock")
        keyboard.release("caps lock")
    

def language_adjustment(keysSock):
    isEnglish = is_english()
    isServerEnglish = int(keysSock.recv(1).decode())
    if (isEnglish and not isServerEnglish) or (not isEnglish and isServerEnglish):
        keyboard.press("shift")
        keyboard.press("alt")
        keyboard.release("shift")
        keyboard.release("alt")



def handleKeysAndMouse(keysOrMouseSock, keysOrMouseSock_address):
    while True:
        message_type = keysOrMouseSock.recv(1).decode()
        if message_type == "1":
            press_key(keysOrMouseSock)
        elif message_type == "2":
            release_key(keysOrMouseSock)
        elif message_type == "3":
            handle_mouse()
        elif message_type == "4":
            capslock_adjustment(keysOrMouseSock)
        elif message_type == "5":
            language_adjustment(keysOrMouseSock)




if __name__ == "__main__":
    keysPort = 9200
    keysSock = My_Server(listen_port=keysPort, simultaneous_requests_limit=2, handle=handleKeysAndMouse, is_secured=True)
    t2 = threading.Thread(target=keysSock.start)
    t2.start()


    # screenshot_server_ip = "127.0.0.1" 
    screenshot_server_ip = "10.0.0.35"   # when I'm using my Desktop computer as Server.py and I'm at home
    screenshot_server_Port = 9124
    screenshotSock = connect_My_Server(screenshot_server_ip, screenshot_server_Port)

    #screenshotLoop(screenshotSock)
    
