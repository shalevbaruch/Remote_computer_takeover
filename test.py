
from pynput.keyboard import Key, Listener, Controller

# keyboard = Controller()
import win32con
import win32api
from ctypes import windll

def char2key(c):
    result = windll.User32.VkKeyScanW(ord(str(c)))
    shift_state = (result & 0xFF00) >> 8
    vk_key = result & 0xFF

    return vk_key


# def show(key):
 
#     print('\nYou Entered {0}'.format( key))
#     keyboard.press(key)
#     return False
 
# Collect all event until released
# with Listener(on_press = show) as listener:  
#     listener.join()
# exit()

# key = ord(getch())
# print(key)


VK_CODE = char2key('a')
print(VK_CODE)
#win32api.keybd_event(VK_CODE, 0, 0, 0)  # simulate key down
#win32api.keybd_event(VK_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)  # simulate key up
win32api.keybd_event(65, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
