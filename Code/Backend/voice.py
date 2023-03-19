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
    nombre_pin ={1:"Pin 1",2:"Pin 2",4:"Pin 3",8:"Pin 4",16:"Pin 5",32:"Pin 6",64:"Pin 7",128:"Pin 8"}
    if(key[1] in nombre_pin.keys()):
        q.put(nombre_pin[key[1]])    

def hid_loop():
    t = Thread(target=say_loop)
    t.daemon = True
    t.start()
    for device in hid.enumerate():
        print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
    if 'Arduino Leonardo' in device['product_string']:
        dir1,dir2 = device['vendor_id'], device['product_id']
        gamepad = hid.device()
        gamepad.open(dir1,dir2)
        gamepad.set_nonblocking(True)
        while True:
            report = gamepad.read(64)
            if report:
                #print(report) #Muestra la cadena enviada por el Arduino según las fotopuertas
                key_recorder(report)
                time.sleep(1)
    else:
        print('"Joystick" no encontrado')
constant_reader = Thread(target=hid_loop)
constant_reader.start()
q.join() # ends the loop when queue is empty