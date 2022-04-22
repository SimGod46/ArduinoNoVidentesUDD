from threading import Thread
import pyttsx3, hid, time
from queue import Queue
q = Queue()
def say_loop():
    engine = pyttsx3.init()
    while True:
        engine.say(q.get())
        engine.runAndWait()
        q.task_done()
        
def key_recorder(key):
    if key[0] == 0:
        q.put('Pin 1')
    elif key[0] == 255:
        q.put('Pin 2')
    elif key[1] == 0:
        q.put('Pin 3')
    elif key[5] == 79:
        q.put('Boton x')    

def hid_loop():
    t = Thread(target=say_loop)
    t.daemon = True
    t.start()
    for device in hid.enumerate():
        print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
    if 'Generic   USB  Joystick' in device['product_string']:
        dir1,dir2 = device['vendor_id'], device['product_id']
        gamepad = hid.device()
        gamepad.open(dir1,dir2)
        gamepad.set_nonblocking(True)
        while True:
            report = gamepad.read(64)
            if report:
                #print(report)
                key_recorder(report)
                time.sleep(1)
    else:
        print('"Joystick" no encontrado')
constant_reader = Thread(target=hid_loop)
constant_reader.start()
q.join() # ends the loop when queue is empty