import sys
sys.path.append("C:/University")  # This is the path on my desktop computer
sys.path.append("C:/University/Cyber/networks")  #This is the path on my laptop
import threading
import keyboard
import socket
import ssl
import ctypes
import tkinter as tk
from pynput.mouse import Listener

try:
    from Sending_Files_System.general_server import My_Server
except ImportError:
    from ..Sending_Files_System.general_server import My_Server


first_screenshot = True 
client_listening_port = 9200
client_ip = "10.0.0.60"
keysSock = None
mouseSock = None
client_width = 0
client_height = 0
server_width = 1920
server_height = 1080


#set the GUI
root = tk.Tk()
screenshot_label = tk.Label(root)
screenshot_label.pack()
run_mainloop = True
root.attributes('-fullscreen',True)


def click(x,y,button,pressed):
    print("Mouse is Clicked at (",x,",",y,")","with",button)
    global mouseSock
    if pressed:
        mouseSock.sendall("3".encode())
    else:
        mouseSock.sendall("4".encode())
    x = max(x,0)
    y = max(y,0)
    (x,y) = adjust_res(x,y)
    x = x.to_bytes(4, byteorder='big')
    y = y.to_bytes(4, byteorder='big')
    button_len = len(button.name).to_bytes(4, byteorder='big')
    message = x + y + button_len + button.name.encode()
    mouseSock.sendall(message)
    

def adjust_res(width, height):
    global client_height
    global client_width
    global server_width
    global server_height
    x = int(width * (server_width/client_width))
    y = int(height * (server_height/client_height))
    return (x,y)


def movement(x,y):
    global mouseSock
    x = max(x,0)
    y = max(y,0)
    (x,y) = adjust_res(x,y)
    mouseSock.sendall("5".encode())
    mouseSock.sendall(x.to_bytes(4, byteorder='big'))
    mouseSock.sendall(y.to_bytes(4, byteorder='big'))


def handleScreenshot(ssl_client_soc, ssl_client_soc_address):
    global first_screenshot
    global keysSock
    global mouseSock
    global root
    global screenshot_label
    global run_mainloop
    global client_width
    global client_height
    if first_screenshot:
        first_screenshot = False

        client_width = ssl_client_soc.recv(4)
        client_width = int.from_bytes(client_width, byteorder='big')

        client_height = ssl_client_soc.recv(4)
        client_height = int.from_bytes(client_height, byteorder='big')
        
        keysSock = connect_My_Server(client_ip, client_listening_port)
        t1  = threading.Thread(target=sendKeys)
        t1.start()

        mouseSock = connect_My_Server(client_ip, client_listening_port)
        t2 = Listener(on_click=click, on_move=movement)
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
    screenshot_image = tk.PhotoImage(data=screenshot)
    screenshot_label.config(image=screenshot_image)
    screenshot_label.image = screenshot_image # Keep a reference to the image to prevent garbage collection
    root.after(2, handleScreenshot, ssl_client_soc, ssl_client_soc_address) # Schedule the next call to this function in 1000 milliseconds (1 second)
    if run_mainloop:
        run_mainloop = False
        root.mainloop()
        


def sendKeys():
    while True:
        event = keyboard.read_event()
        event_type = event.event_type
        event_name = event.name

        if event_type == "down":
            keysSock.sendall("1".encode())
        elif event_type == "up":
            keysSock.sendall("2".encode())

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



