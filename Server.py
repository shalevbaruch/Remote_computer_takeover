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

hebrew_to_english = {
    'א': "t", 'ב': 'c', 'ג': 'd', 'ד': 's', 'ה': 'v', 'ו': 'u', 'ז': 'z',
    'ח': 'j', 'ט': 'y', 'י': 'h', 'כ': 'f', 'ל': 'k', 'מ': 'n', 'נ': 'b',
    'ס': 'x', 'ע': 'g', 'פ': 'p', 'צ': 'm', 'ק': 'e', 'ר': 'r', 'ש': 'a',
    'ת': ',', 'ם': 'o', 'ן': 'i', 'ץ': '.', 'ף': ';', 'ך': 'l', ";" : "`",
     "[" : "]", "]" : "[", "{" : "}", "}": "{", "(" : ")", ")" : "(", 
      "," : "'", "." : "/" , "'": "w", "/" : "q"
}

# , ";" : "`",
#     "[" : "]", "]" : "[", "{" : "}", "}": "{", "(" : ")", ")" : "(", 
#    "," : "'", "." : "/" , "'": "w", "/" : "q"
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


def sendKeys():
    
    global hebrew_to_english
    # adjustment of caps lock
    # keysSock.sendall("4".encode())
    # capslock_on = is_capslock_on()
    # if capslock_on:
    #     keysSock.sendall("1".encode())
    # else:
    #     keysSock.sendall("0".encode())

    # # adjustment of language
    # keysSock.sendall("5".encode())
    # isEnglish = is_english()
    # if isEnglish:
    #     keysSock.sendall("1".encode())
    # else:
    #     keysSock.sendall("0".encode())
    # isEnglish = is_english()
    # keysSock.sendall("6".encode())
    # capslock_on = is_capslock_on()
    # if capslock_on:
    #     keysSock.sendall("1".encode())
    # else:
    #     keysSock.sendall("0".encode())
    # isClientEnglish = int(keysSock.recv(1).decode())
    # if (isClientEnglish and not isEnglish) or (not isClientEnglish and isEnglish):
    #     keyboard.press("shift")
    #     keyboard.press("alt")
    #     keyboard.release("shift")
    #     keyboard.release("alt")
    

    while True:
        event = keyboard.read_event()
        event_type = event.event_type
        event_name = event.name
        # if event_name in hebrew_to_english:
        #     event_name = hebrew_to_english[event_name]
        if event_type == "down":
            keysSock.sendall("1".encode())
        elif event_type == "up":
            keysSock.sendall("2".encode())
        # if event_name in hebrew_to_english:
        #     keysSock.sendall(len(event_name + " ").to_bytes(4, byteorder='big'))
        #     keysSock.sendall(event_name.encode())
        # else:
        #     keysSock.sendall(len(event_name).to_bytes(4, byteorder='big'))
        #     keysSock.sendall(event_name.encode())
        if len(event_name) == 1:
            keysSock.sendall("1".encode())
            scancode = convert_to_scancode(event_name)
            message_length = 4
            keysSock.sendall(message_length.to_bytes(4, byteorder='big'))
            keysSock.sendall(scancode.to_bytes(4, byteorder='big'))
        else:
            keysSock.sendall("0".encode())
            keysSock.sendall(len(event_name).to_bytes(4, byteorder='big'))
            keysSock.sendall(event_name.encode())



def sendMouse(mouseSock):
    pass


def convert_to_scancode(key):
    result = ctypes.windll.User32.VkKeyScanW(ord(key))
    vk_key = result & 0xFF
    return vk_key





def connect_My_Server(Server_IP, Server_Port):
    server_address = (Server_IP, Server_Port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock)  # add a security layer
    ssl_sock.connect(server_address)    
    return ssl_sock


if __name__ == '__main__':
    screenshotServer = My_Server(listen_port=9124, simultaneous_requests_limit=1, handle=handleScreenshot, is_secured=True)
    screenshotServer.start()



