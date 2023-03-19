from recognize import modules_recognizer
from dbms import data_manager
import voice,cv2
cap = cv2.VideoCapture(1) #Cambiar a 1 para utilizar arduino
height = 224#int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = 224#int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
reconocedor_img = modules_recognizer()
base_datos = data_manager()
while True:
    tomar_foto = input('> ')
    if tomar_foto == '':
        ret, frame = cap.read()
        cv2.imwrite('module.jpg',frame)
        cv2.imshow('image',frame)
        # reconocimiento
        module_detected= reconocedor_img.read('module.jpg')
        print('Detectado: ',module_detected)
        module_info = base_datos.query_module(module_detected) #
        voice.q.put(module_info)
        print('_____')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break