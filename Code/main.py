from recognize import modules_recognizer
from dbms import data_manager
import voice,cv2
cap = cv2.VideoCapture(0) #Cambiar a 1
height = 224#int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = 224#int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
while True:
    tomar_foto = input('> ')
    if tomar_foto == '':
        ret, frame = cap.read()
        print('Photo taken!')
        cv2.imwrite('module.jpg',frame)
        # reconocimiento
        module_detected= modules_recognizer.read('module.jpg')
        module_info = data_manager.query_module(module_detected) #
        voice.q.put(module_info)
        print('_____')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break