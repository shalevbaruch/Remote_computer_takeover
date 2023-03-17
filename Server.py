import sys
sys.path.append("C:/University")  # This is the path on my desktop computer
sys.path.append("C:/University/YoungForTech/networks")  #Thie is the path on my laptop
import os
import threading
import keyboard
import time
import socket
import ssl

try:
    from Sending_Files_System.server import My_Server
except ImportError:
    from ..Sending_Files_System.server import My_Server


def handleScreenshot(server, ssl_client_soc):
    # key = keyboard.read_event()
    screenshot_size = ssl_client_soc.recv(4)
    screenshot_size = int.from_bytes(screenshot_size, byteorder='big')
    print("new image with size: {}".format(screenshot_size))
    screenshot = b''
    bytes_recieved = 0 
    while bytes_recieved < screenshot_size:
        screenshot_part =  ssl_client_soc.recv(1024)
        screenshot += screenshot_part
        bytes_recieved += len(screenshot_part)
    print(screenshot[0:100])
    print(len(screenshot))
    print("finished")


def sendKeys(keysSock):
    while True:
        try: 
            key = keyboard.read_event()
            print(key.event_type)
            if key.event_type == 'down':
                keysSock.send(key.name.encode())
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


def connect_My_Server(Server_IP, Server_Port, Transport_Layer_Protocol):
    server_address = (Server_IP, Server_Port)
    if Transport_Layer_Protocol == "UDP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    else:  # Transport_Layer_Protocol == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(sock)  # add a security layer
        ssl_sock.connect(server_address)     
    return ssl_sock



# if Keyboard:
#     dsadsa
# elif mouse:
#     sadsada


if __name__ == '__main__':
    # keyboard_server_ip =  "10.0.0.60"  # when I'm using my laptop as the customer and I'm at home (The IP will probable change if I am at Tel-Aviv)
    # keyboard_server_port = 9200
    # Transport_Layer_Protocol = "TCP"
    # keyboard_sock = connect_My_Server(keyboard_server_ip, keyboard_server_port, Transport_Layer_Protocol)



    
    screenshotServer = My_Server(LISTEN_PORT=9124, SIMULTANEOUS_REQUESTS_LIMIT=1,TRANSPORT_LAYER_PROTOCOL="TCP", HANDLE=handleScreenshot, RUNS_ONCE=connect_My_Server)
    screenshotServer.start()
    # t1 = threading.Thread(target=screenshotServer.start)
    # t1.start()


    # # keyboard_server_ip = "127.0.0.1"

    # # while True:
    #     # if can_continue:
    
    # t2 =threading.Thread(target=sendKeys, args=(keyboard_sock,)) 
    # t2.start()
    
    
    # t1.join()
    # t2.join()