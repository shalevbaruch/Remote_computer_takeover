import sys
sys.path.append("C:/University")  # This is the path on my desktop computer
sys.path.append("C:/University/Cyber/networks")  #Thie is the path on my laptop
import os
import threading
import keyboard
import time
import socket
import ssl

try:
    from Sending_Files_System.general_server import My_Server
except ImportError:
    from ..Sending_Files_System.general_server import My_Server


first_screenshot = True # when we get the first screenshot, it means the client already set up the server for mouse and keyboard
client_listening_port = 9200
client_listening_ip = "10.0.0.138"


def handleScreenshot(ssl_client_soc, ssl_client_soc_address):
    if first_screenshot:
        first_screenshot = False
        t1  = threading.Thread()
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


def sendKeys(keysSock):
    while True:
        try: 
            key = keyboard.read_event()
            print(key.event_type)
            if key.event_type == 'down':
                keysSock.sendall(len(key.name).to_bytes(4, byteorder='big')) 
                keysSock.sendall(key.name.encode())
        except:
            break


def sendkeys2(sock):
    while True:
        try:
            event = keyboard.read_event()
            # check if the event is a key down event
            if event.event_type == "down":
                # get the key name, including special keys like ctrl+z
                key_name = keyboard.key_to_scan_codes(event.name)[0]
                # send the key name to the server
                message = f"{key_name}".encode()
                sock.sendall(message)
        except KeyboardInterrupt:
            # close the socket and exit the loop
            sock.close()
            break


def connect_My_Server(Server_IP, Server_Port):
    server_address = (Server_IP, Server_Port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock)  # add a security layer
    ssl_sock.connect(server_address)    
    return ssl_sock


if __name__ == '__main__':
    screenshotServer = My_Server(listen_port=9124, simultaneous_requests_limit=1, handle=handleScreenshot, is_secured=True)
    screenshotServer.start()



