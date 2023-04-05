import keyboard
from pynput.keyboard import Key, Listener


def on_press(key):
    key_repr = key.char if hasattr(key, 'char') else key.name
    

def on_release(key):
    key_repr = key.char if hasattr(key, 'char') else key.name
    


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

