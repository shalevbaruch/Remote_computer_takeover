import sys
sys.path.append("C:/University/YoungForTech/networks")
import keyboard
import os
try:
    from Sending_Files_System.server import My_Server
except ImportError:
    from ..Sending_Files_System.server import My_Server


def handle(server, ssl_client_soc, command_option, client_msg):
    # key = keyboard.read_event()
    screenshot_size = ssl_client_soc.recv(4)
    size = int.from_bytes(screenshot_size, byteorder='big')
    screenshot = b''
    bytes_recieved = 0 
    with open(os.path.join("C:/University/YoungForTech/networks/Remote_computer_takeover", "screen.txt"), 'wb') as file_to_write:
        while bytes_recieved < screenshot_size:
            screenshot_part =  ssl_client_soc.recv(1024)
            screenshot += screenshot_part
            file_to_write.write(screenshot_part)
            bytes_recieved += len(screenshot_part)


if __name__ == '__main__':
    server = My_Server(LISTEN_PORT=9124, SIMULTANEOUS_REQUESTS_LIMIT=5,HANDLE=handle)
    server.start()