import pyttsx3, hid, time
from queue import Queue
from threading import Thread

q = Queue()

def key_recorder(key):
    if key[1] == 1:
        q.put('D0')
        time.sleep(1)
    elif key[1] == 2:
        q.put('D1')
        time.sleep(1)
    elif key[1] == 4:
        q.put('A0')
        time.sleep(1)
    elif key[1] == 8:
        q.put('A1')
        time.sleep(1)
    elif key[1] == 16:
        q.put('VCC')
        time.sleep(1)
    elif key[1] == 32:
        q.put('VCC')
        time.sleep(1)
    elif key[1] == 64:
        q.put('GND')
        time.sleep(1)
    elif key[1] == 128:
        q.put('GND')
        time.sleep(1)

def say_loop():
    engine = pyttsx3.init()
    while True:
        engine.say(q.get())
        engine.runAndWait()
        q.task_done()

def joystick_loop():
    t = Thread(target=say_loop)
    t.daemon = True
    t.start()

    for device in hid.enumerate():
        print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

        if 'Leonardo' in device['product_string']:
            dir1,dir2 = device['vendor_id'], device['product_id']
            gamepad = hid.device()
            gamepad.open(dir1,dir2)
            gamepad.set_nonblocking(True)
            while True:
                report = gamepad.read(64)
                if report:
                    print(report)
                    key_recorder(report)
    #                time.sleep(0.01)


if __name__=="__main__":
    joystick_loop()
    q.join() # ends the loop when queue is empty