import sys
sys.path.append("C:/University/YoungForTech/networks")
import keyboard
import os
import threading

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


def sendKeys(keysServer, keysSock):
    message = keysSock.recv(20).decode()
    print(message)
    while True:
        try: 
            key = keyboard.read_event()
            if key.event_type == 'down':
                keysSock.send(key.name.encode())
        except:
            break






if __name__ == '__main__':
    screenshotServer = My_Server(LISTEN_PORT=9124, SIMULTANEOUS_REQUESTS_LIMIT=1,TRANSPORT_LAYER_PROTOCOL="TCP", HANDLE=handleScreenshot)
    t1 = threading.Thread(target=screenshotServer.start)
    t1.start()
    t1.join()

    # keyboardServer = My_Server(LISTEN_PORT=9200, SIMULTANEOUS_REQUESTS_LIMIT=2,TRANSPORT_LAYER_PROTOCOL="TCP", HANDLE=sendKeys)
    # keyboardServer.start()
    # t2 = threading.Thread(target=keyboardServer.start)
    # t2.start()
    # t2.join()
    # screenshotServer.start()
    
    # t1.join()